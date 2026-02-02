from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional
from datetime import datetime, timedelta, date
import uuid
import json

from database import get_db
import models

router = APIRouter(prefix="/pharmacy", tags=["pharmacy"])

# ==================== UTILITY FUNCTIONS ====================

def generate_drug_code():
    return f"DRG-{uuid.uuid4().hex[:8].upper()}"

def generate_po_number():
    return f"PO-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"

def generate_transaction_id():
    return f"TX-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:3].upper()}"

def check_drug_interactions(drug_ids: List[str], db: Session):
    """Check for drug interactions between multiple drugs"""
    interactions = []
    for i in range(len(drug_ids)):
        for j in range(i + 1, len(drug_ids)):
            interaction = db.query(models.DrugInteraction).filter(
                or_(
                    and_(
                        models.DrugInteraction.drug1_id == drug_ids[i],
                        models.DrugInteraction.drug2_id == drug_ids[j]
                    ),
                    and_(
                        models.DrugInteraction.drug1_id == drug_ids[j],
                        models.DrugInteraction.drug2_id == drug_ids[i]
                    )
                )
            ).first()
            
            if interaction:
                interactions.append(interaction.to_dict())
    
    return interactions

def check_inventory_availability(drug_id: str, quantity: int, db: Session):
    """Check if enough stock is available"""
    inventory = db.query(models.Inventory).filter(
        models.Inventory.drug_id == drug_id,
        models.Inventory.quantity >= quantity
    ).first()
    
    return inventory is not None

# ==================== DRUG ENDPOINTS ====================

@router.get("/drugs", response_model=dict)
def get_drugs(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    category: Optional[str] = None,
    prescription_required: Optional[bool] = None,
    in_stock_only: bool = False,
    db: Session = Depends(get_db)
):
    """Get list of drugs with optional filters"""
    query = db.query(models.Drug)
    
    if search:
        query = query.filter(
            or_(
                models.Drug.brand_name.ilike(f"%{search}%"),
                models.Drug.generic_name.ilike(f"%{search}%"),
                models.Drug.drug_code.ilike(f"%{search}%")
            )
        )
    
    if category:
        query = query.filter(models.Drug.category.ilike(f"%{category}%"))
    
    if prescription_required is not None:
        query = query.filter(models.Drug.prescription_required == prescription_required)
    
    if in_stock_only:
        # Join with inventory to check stock
        query = query.join(models.Inventory).filter(models.Inventory.quantity > 0)
    
    total = query.count()
    drugs = query.offset(skip).limit(limit).all()
    
    return {
        "count": total,
        "drugs": [drug.to_dict() for drug in drugs]
    }

@router.get("/drugs/{drug_id}", response_model=dict)
def get_drug(drug_id: str, db: Session = Depends(get_db)):
    """Get specific drug by ID"""
    drug = db.query(models.Drug).filter(models.Drug.id == drug_id).first()
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    
    return drug.to_dict()

@router.post("/drugs", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_drug(
    brand_name: str,
    generic_name: str,
    drug_type: str,
    strength: str,
    unit: str,
    category: str,
    manufacturer: str,
    prescription_required: bool = True,
    schedule: Optional[str] = None,
    storage_conditions: Optional[str] = None,
    side_effects: Optional[str] = None,
    contraindications: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Create a new drug"""
    try:
        # Generate unique drug code
        drug_code = generate_drug_code()
        
        drug = models.Drug(
            id=str(uuid.uuid4()),
            drug_code=drug_code,
            brand_name=brand_name,
            generic_name=generic_name,
            manufacturer=manufacturer,
            drug_type=drug_type,
            strength=strength,
            unit=unit,
            category=category,
            prescription_required=prescription_required,
            schedule=schedule,
            storage_conditions=storage_conditions,
            side_effects=side_effects,
            contraindications=contraindications,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_active=True
        )
        
        db.add(drug)
        db.commit()
        db.refresh(drug)
        
        return {
            "message": "Drug created successfully",
            "drug_id": drug.id,
            "drug_code": drug.drug_code,
            "drug": drug.to_dict()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating drug: {str(e)}")

@router.put("/drugs/{drug_id}", response_model=dict)
def update_drug(
    drug_id: str,
    brand_name: Optional[str] = None,
    generic_name: Optional[str] = None,
    strength: Optional[str] = None,
    unit_price: Optional[float] = None,
    selling_price: Optional[float] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Update drug information"""
    drug = db.query(models.Drug).filter(models.Drug.id == drug_id).first()
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    
    try:
        if brand_name:
            drug.brand_name = brand_name
        if generic_name:
            drug.generic_name = generic_name
        if strength:
            drug.strength = strength
        if is_active is not None:
            drug.is_active = is_active
        
        drug.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(drug)
        
        # Update inventory prices if provided
        if unit_price is not None or selling_price is not None:
            inventory = db.query(models.Inventory).filter(
                models.Inventory.drug_id == drug_id
            ).first()
            
            if inventory:
                if unit_price is not None:
                    inventory.unit_price = unit_price
                if selling_price is not None:
                    inventory.selling_price = selling_price
                db.commit()
        
        return {
            "message": "Drug updated successfully",
            "drug": drug.to_dict()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating drug: {str(e)}")

# ==================== INVENTORY ENDPOINTS ====================

@router.get("/inventory", response_model=dict)
def get_inventory(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,  # in_stock, low_stock, out_of_stock, expired
    drug_id: Optional[str] = None,
    expiry_threshold_days: Optional[int] = 30,
    db: Session = Depends(get_db)
):
    """Get inventory list with filters"""
    query = db.query(models.Inventory).join(models.Drug)
    
    if drug_id:
        query = query.filter(models.Inventory.drug_id == drug_id)
    
    # Apply status filter
    if status:
        now = datetime.utcnow()
        if status == "expired":
            query = query.filter(models.Inventory.expiry_date < now)
        elif status == "low_stock":
            query = query.filter(
                models.Inventory.quantity <= models.Inventory.reorder_level,
                models.Inventory.quantity > 0
            )
        elif status == "out_of_stock":
            query = query.filter(models.Inventory.quantity <= 0)
        elif status == "in_stock":
            query = query.filter(
                models.Inventory.quantity > models.Inventory.reorder_level,
                models.Inventory.expiry_date > now
            )
    
    # Filter for expiring soon
    if expiry_threshold_days:
        threshold_date = datetime.utcnow() + timedelta(days=expiry_threshold_days)
        query = query.filter(models.Inventory.expiry_date <= threshold_date)
    
    total = query.count()
    inventory_items = query.offset(skip).limit(limit).all()
    
    return {
        "count": total,
        "inventory": [item.to_dict() for item in inventory_items]
    }

@router.post("/inventory", response_model=dict, status_code=status.HTTP_201_CREATED)
def add_to_inventory(
    drug_id: str,
    batch_number: str,
    quantity: int,
    unit_price: float,
    selling_price: float,
    expiry_date: str,
    supplier_id: Optional[str] = None,
    location: Optional[str] = None,
    reorder_level: Optional[int] = None,
    reorder_quantity: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Add or update inventory for a drug"""
    try:
        # Parse expiry date
        expiry = datetime.strptime(expiry_date, "%Y-%m-%d")
        
        # Check if drug exists
        drug = db.query(models.Drug).filter(models.Drug.id == drug_id).first()
        if not drug:
            raise HTTPException(status_code=404, detail="Drug not found")
        
        # Check if inventory already exists for this drug
        existing_inventory = db.query(models.Inventory).filter(
            models.Inventory.drug_id == drug_id
        ).first()
        
        if existing_inventory:
            # Update existing inventory
            existing_inventory.quantity += quantity
            existing_inventory.unit_price = unit_price
            existing_inventory.selling_price = selling_price
            existing_inventory.expiry_date = expiry
            existing_inventory.supplier_id = supplier_id
            existing_inventory.location = location
            existing_inventory.last_restocked = datetime.utcnow()
            existing_inventory.updated_at = datetime.utcnow()
            
            if reorder_level:
                existing_inventory.reorder_level = reorder_level
            if reorder_quantity:
                existing_inventory.reorder_quantity = reorder_quantity
            
            inventory = existing_inventory
        else:
            # Create new inventory
            inventory = models.Inventory(
                id=str(uuid.uuid4()),
                drug_id=drug_id,
                batch_number=batch_number,
                quantity=quantity,
                reorder_level=reorder_level or 10,
                reorder_quantity=reorder_quantity or 100,
                unit_price=unit_price,
                selling_price=selling_price,
                expiry_date=expiry,
                supplier_id=supplier_id,
                location=location,
                last_restocked=datetime.utcnow(),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(inventory)
        
        # Create stock transaction
        transaction = models.StockTransaction(
            id=str(uuid.uuid4()),
            transaction_id=generate_transaction_id(),
            inventory_id=inventory.id,
            transaction_type="purchase",
            quantity=quantity,
            unit_price=unit_price,
            total_price=quantity * unit_price,
            reference_id="MANUAL_ADD",
            reference_type="manual",
            notes="Manual inventory addition",
            created_by="system",
            created_at=datetime.utcnow()
        )
        db.add(transaction)
        
        db.commit()
        db.refresh(inventory)
        
        return {
            "message": "Inventory updated successfully",
            "inventory": inventory.to_dict()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating inventory: {str(e)}")

@router.get("/inventory/low-stock", response_model=dict)
def get_low_stock_items(db: Session = Depends(get_db)):
    """Get items that need reordering"""
    low_stock_items = db.query(models.Inventory).filter(
        models.Inventory.quantity <= models.Inventory.reorder_level,
        models.Inventory.quantity > 0
    ).all()
    
    expired_items = db.query(models.Inventory).filter(
        models.Inventory.expiry_date < datetime.utcnow()
    ).all()
    
    return {
        "low_stock": [item.to_dict() for item in low_stock_items],
        "expired": [item.to_dict() for item in expired_items],
        "total_low_stock": len(low_stock_items),
        "total_expired": len(expired_items)
    }

@router.get("/inventory/expiring-soon", response_model=dict)
def get_expiring_soon(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get items expiring within specified days"""
    threshold_date = datetime.utcnow() + timedelta(days=days)
    
    expiring_items = db.query(models.Inventory).filter(
        models.Inventory.expiry_date <= threshold_date,
        models.Inventory.expiry_date > datetime.utcnow()
    ).all()
    
    return {
        "expiring_within_days": days,
        "items": [item.to_dict() for item in expiring_items],
        "count": len(expiring_items)
    }

# ==================== PRESCRIPTION ENDPOINTS ====================

@router.get("/prescriptions", response_model=dict)
def get_prescriptions(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    patient_id: Optional[str] = None,
    doctor_id: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get prescriptions with filters"""
    query = db.query(models.Prescription)
    
    if status:
        query = query.filter(models.Prescription.status == status)
    
    if patient_id:
        query = query.filter(models.Prescription.patient_id == patient_id)
    
    if doctor_id:
        query = query.filter(models.Prescription.doctor_id == doctor_id)
    
    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.filter(models.Prescription.date_prescribed >= start)
    
    if end_date:
        end = datetime.strptime(end_date, "%Y-%m-%d")
        query = query.filter(models.Prescription.date_prescribed <= end)
    
    total = query.count()
    prescriptions = query.offset(skip).limit(limit).all()
    
    return {
        "count": total,
        "prescriptions": [prescription.to_dict() for prescription in prescriptions]
    }

@router.post("/prescriptions", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_prescription(
    patient_id: str,
    doctor_id: str,
    items: List[dict],
    validity_days: int = 30,
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Create a new prescription"""
    try:
        # Check if patient exists
        patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        # Check if doctor exists
        doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        
        # Check for drug interactions
        drug_ids = [item["drug_id"] for item in items]
        interactions = check_drug_interactions(drug_ids, db)
        
        if interactions:
            # Return warning but allow creation
            pass
        
        # Create prescription
        prescription = models.Prescription(
            id=str(uuid.uuid4()),
            prescription_number=f"RX-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}",
            patient_id=patient_id,
            doctor_id=doctor_id,
            date_prescribed=datetime.utcnow(),
            status="active",
            validity_days=validity_days,
            notes=notes,
            created_at=datetime.utcnow()
        )
        db.add(prescription)
        
        # Add prescription items
        for item in items:
            prescription_item = models.PrescriptionItem(
                id=str(uuid.uuid4()),
                prescription_id=prescription.id,
                drug_id=item["drug_id"],
                quantity=item["quantity"],
                dosage=item.get("dosage"),
                frequency=item.get("frequency"),
                duration=item.get("duration"),
                instructions=item.get("instructions"),
                status="pending",
                created_at=datetime.utcnow()
            )
            db.add(prescription_item)
        
        db.commit()
        db.refresh(prescription)
        
        return {
            "message": "Prescription created successfully",
            "prescription_id": prescription.id,
            "prescription_number": prescription.prescription_number,
            "interaction_warnings": interactions,
            "prescription": prescription.to_dict()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating prescription: {str(e)}")

@router.post("/prescriptions/{prescription_id}/dispense", response_model=dict)
def dispense_prescription(
    prescription_id: str,
    dispensed_by: str,
    db: Session = Depends(get_db)
):
    """Dispense a prescription"""
    try:
        prescription = db.query(models.Prescription).filter(
            models.Prescription.id == prescription_id
        ).first()
        
        if not prescription:
            raise HTTPException(status_code=404, detail="Prescription not found")
        
        if prescription.status != "active":
            raise HTTPException(status_code=400, detail="Prescription is not active")
        
        # Check inventory for all items
        for item in prescription.items:
            if not check_inventory_availability(item.drug_id, item.quantity, db):
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for drug ID: {item.drug_id}"
                )
        
        # Dispense each item
        for item in prescription.items:
            # Update inventory
            inventory = db.query(models.Inventory).filter(
                models.Inventory.drug_id == item.drug_id
            ).first()
            
            inventory.quantity -= item.quantity
            inventory.updated_at = datetime.utcnow()
            
            # Update prescription item
            item.status = "dispensed"
            item.dispensed_by = dispensed_by
            item.dispensed_at = datetime.utcnow()
            
            # Create stock transaction
            transaction = models.StockTransaction(
                id=str(uuid.uuid4()),
                transaction_id=generate_transaction_id(),
                inventory_id=inventory.id,
                transaction_type="sale",
                quantity=item.quantity,
                unit_price=inventory.selling_price,
                total_price=item.quantity * inventory.selling_price,
                reference_id=prescription.prescription_number,
                reference_type="prescription",
                notes=f"Dispensed prescription {prescription.prescription_number}",
                created_by=dispensed_by,
                created_at=datetime.utcnow()
            )
            db.add(transaction)
        
        # Update prescription status
        prescription.status = "dispensed"
        prescription.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "message": "Prescription dispensed successfully",
            "prescription": prescription.to_dict()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error dispensing prescription: {str(e)}")

# ==================== DRUG INTERACTION ENDPOINTS ====================

@router.get("/drug-interactions/check", response_model=dict)
def check_interactions(
    drug_ids: List[str] = Query(...),
    db: Session = Depends(get_db)
):
    """Check interactions between multiple drugs"""
    interactions = check_drug_interactions(drug_ids, db)
    
    return {
        "drug_ids": drug_ids,
        "interactions_found": len(interactions),
        "interactions": interactions
    }

@router.post("/drug-interactions", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_drug_interaction(
    drug1_id: str,
    drug2_id: str,
    severity: str,
    description: str,
    mechanism: Optional[str] = None,
    management: Optional[str] = None,
    evidence_level: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Create a new drug interaction record"""
    try:
        # Check if drugs exist
        drug1 = db.query(models.Drug).filter(models.Drug.id == drug1_id).first()
        drug2 = db.query(models.Drug).filter(models.Drug.id == drug2_id).first()
        
        if not drug1 or not drug2:
            raise HTTPException(status_code=404, detail="One or both drugs not found")
        
        # Check if interaction already exists
        existing = db.query(models.DrugInteraction).filter(
            or_(
                and_(
                    models.DrugInteraction.drug1_id == drug1_id,
                    models.DrugInteraction.drug2_id == drug2_id
                ),
                and_(
                    models.DrugInteraction.drug1_id == drug2_id,
                    models.DrugInteraction.drug2_id == drug1_id
                )
            )
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="Interaction already exists")
        
        interaction = models.DrugInteraction(
            id=str(uuid.uuid4()),
            drug1_id=drug1_id,
            drug2_id=drug2_id,
            severity=severity,
            description=description,
            mechanism=mechanism,
            management=management,
            evidence_level=evidence_level,
            created_at=datetime.utcnow()
        )
        
        db.add(interaction)
        db.commit()
        db.refresh(interaction)
        
        return {
            "message": "Drug interaction created successfully",
            "interaction": interaction.to_dict()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating drug interaction: {str(e)}")

# ==================== SUPPLIER ENDPOINTS ====================

@router.get("/suppliers", response_model=dict)
def get_suppliers(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of suppliers"""
    query = db.query(models.Supplier)
    
    if active_only:
        query = query.filter(models.Supplier.is_active == True)
    
    if search:
        query = query.filter(
            or_(
                models.Supplier.name.ilike(f"%{search}%"),
                models.Supplier.supplier_code.ilike(f"%{search}%"),
                models.Supplier.contact_person.ilike(f"%{search}%")
            )
        )
    
    total = query.count()
    suppliers = query.offset(skip).limit(limit).all()
    
    return {
        "count": total,
        "suppliers": [supplier.to_dict() for supplier in suppliers]
    }

@router.post("/suppliers", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_supplier(
    name: str,
    contact_person: str,
    email: str,
    phone: str,
    address: str,
    tax_id: Optional[str] = None,
    payment_terms: Optional[str] = None,
    delivery_time: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Create a new supplier"""
    try:
        # Generate supplier code
        supplier_code = f"SUP-{uuid.uuid4().hex[:8].upper()}"
        
        supplier = models.Supplier(
            id=str(uuid.uuid4()),
            supplier_code=supplier_code,
            name=name,
            contact_person=contact_person,
            email=email,
            phone=phone,
            address=address,
            tax_id=tax_id,
            payment_terms=payment_terms,
            delivery_time=delivery_time,
            rating=0.0,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(supplier)
        db.commit()
        db.refresh(supplier)
        
        return {
            "message": "Supplier created successfully",
            "supplier_id": supplier.id,
            "supplier_code": supplier.supplier_code,
            "supplier": supplier.to_dict()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating supplier: {str(e)}")

# ==================== PURCHASE ORDER ENDPOINTS ====================

@router.get("/purchase-orders", response_model=dict)
def get_purchase_orders(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    supplier_id: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get purchase orders with filters"""
    query = db.query(models.PurchaseOrder)
    
    if status:
        query = query.filter(models.PurchaseOrder.status == status)
    
    if supplier_id:
        query = query.filter(models.PurchaseOrder.supplier_id == supplier_id)
    
    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.filter(models.PurchaseOrder.order_date >= start)
    
    if end_date:
        end = datetime.strptime(end_date, "%Y-%m-%d")
        query = query.filter(models.PurchaseOrder.order_date <= end)
    
    total = query.count()
    purchase_orders = query.offset(skip).limit(limit).all()
    
    return {
        "count": total,
        "purchase_orders": [po.to_dict() for po in purchase_orders]
    }

@router.post("/purchase-orders", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_purchase_order(
    supplier_id: str,
    items: List[dict],
    expected_delivery: Optional[str] = None,
    notes: Optional[str] = None,
    created_by: str = "system",
    db: Session = Depends(get_db)
):
    """Create a new purchase order"""
    try:
        # Check if supplier exists
        supplier = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")
        
        # Create purchase order
        purchase_order = models.PurchaseOrder(
            id=str(uuid.uuid4()),
            po_number=generate_po_number(),
            supplier_id=supplier_id,
            order_date=datetime.utcnow(),
            expected_delivery=datetime.strptime(expected_delivery, "%Y-%m-%d") if expected_delivery else None,
            status="pending",
            notes=notes,
            created_by=created_by,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(purchase_order)
        
        # Calculate totals
        total_amount = 0.0
        
        # Add purchase order items
        for item in items:
            # Check if drug exists
            drug = db.query(models.Drug).filter(models.Drug.id == item["drug_id"]).first()
            if not drug:
                raise HTTPException(status_code=404, detail=f"Drug not found: {item['drug_id']}")
            
            item_total = item["quantity"] * item["unit_price"]
            total_amount += item_total
            
            po_item = models.PurchaseOrderItem(
                id=str(uuid.uuid4()),
                purchase_order_id=purchase_order.id,
                drug_id=item["drug_id"],
                quantity=item["quantity"],
                unit_price=item["unit_price"],
                total_price=item_total,
                status="pending",
                notes=item.get("notes")
            )
            db.add(po_item)
        
        # Update purchase order totals
        purchase_order.total_amount = total_amount
        purchase_order.grand_total = total_amount
        
        db.commit()
        db.refresh(purchase_order)
        
        return {
            "message": "Purchase order created successfully",
            "purchase_order_id": purchase_order.id,
            "po_number": purchase_order.po_number,
            "purchase_order": purchase_order.to_dict()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating purchase order: {str(e)}")

@router.post("/purchase-orders/{po_id}/receive", response_model=dict)
def receive_purchase_order(
    po_id: str,
    received_items: List[dict],
    received_by: str,
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Receive items from a purchase order"""
    try:
        purchase_order = db.query(models.PurchaseOrder).filter(
            models.PurchaseOrder.id == po_id
        ).first()
        
        if not purchase_order:
            raise HTTPException(status_code=404, detail="Purchase order not found")
        
        if purchase_order.status == "delivered":
            raise HTTPException(status_code=400, detail="Purchase order already delivered")
        
        # Update PO items
        all_received = True
        for received_item in received_items:
            po_item = db.query(models.PurchaseOrderItem).filter(
                models.PurchaseOrderItem.id == received_item["po_item_id"],
                models.PurchaseOrderItem.purchase_order_id == po_id
            ).first()
            
            if not po_item:
                continue
            
            received_qty = received_item["quantity"]
            po_item.received_quantity = received_qty
            
            if received_qty >= po_item.quantity:
                po_item.status = "received"
            elif received_qty > 0:
                po_item.status = "partially_received"
                all_received = False
            else:
                all_received = False
            
            # Update inventory
            inventory = db.query(models.Inventory).filter(
                models.Inventory.drug_id == po_item.drug_id
            ).first()
            
            if inventory:
                inventory.quantity += received_qty
                inventory.last_restocked = datetime.utcnow()
                inventory.updated_at = datetime.utcnow()
            else:
                # Create new inventory entry
                drug = db.query(models.Drug).filter(models.Drug.id == po_item.drug_id).first()
                if drug:
                    inventory = models.Inventory(
                        id=str(uuid.uuid4()),
                        drug_id=po_item.drug_id,
                        batch_number=received_item.get("batch_number", "BATCH-001"),
                        quantity=received_qty,
                        reorder_level=10,
                        reorder_quantity=100,
                        unit_price=po_item.unit_price,
                        selling_price=po_item.unit_price * 1.3,  # 30% markup
                        expiry_date=datetime.utcnow() + timedelta(days=365),  # Default 1 year
                        supplier_id=purchase_order.supplier_id,
                        last_restocked=datetime.utcnow(),
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.add(inventory)
            
            # Create stock transaction
            transaction = models.StockTransaction(
                id=str(uuid.uuid4()),
                transaction_id=generate_transaction_id(),
                inventory_id=inventory.id,
                transaction_type="purchase",
                quantity=received_qty,
                unit_price=po_item.unit_price,
                total_price=received_qty * po_item.unit_price,
                reference_id=purchase_order.po_number,
                reference_type="purchase_order",
                notes=f"Received from PO {purchase_order.po_number}",
                created_by=received_by,
                created_at=datetime.utcnow()
            )
            db.add(transaction)
        
        # Update PO status
        if all_received:
            purchase_order.status = "delivered"
        else:
            purchase_order.status = "partially_delivered"
        
        purchase_order.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "message": "Purchase order received successfully",
            "purchase_order": purchase_order.to_dict()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error receiving purchase order: {str(e)}")

# ==================== REPORTS & ANALYTICS ====================

@router.get("/reports/sales", response_model=dict)
def get_sales_report(
    start_date: str,
    end_date: str,
    group_by: str = "daily",  # daily, weekly, monthly, drug
    db: Session = Depends(get_db)
):
    """Generate sales report"""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    # Query sales transactions
    query = db.query(models.StockTransaction).filter(
        models.StockTransaction.transaction_type == "sale",
        models.StockTransaction.created_at >= start,
        models.StockTransaction.created_at <= end
    )
    
    if group_by == "daily":
        # Group by day
        results = db.query(
            func.date(models.StockTransaction.created_at).label("date"),
            func.sum(models.StockTransaction.total_price).label("total_sales"),
            func.count(models.StockTransaction.id).label("transaction_count"),
            func.sum(models.StockTransaction.quantity).label("total_quantity")
        ).filter(
            models.StockTransaction.transaction_type == "sale",
            models.StockTransaction.created_at >= start,
            models.StockTransaction.created_at <= end
        ).group_by(func.date(models.StockTransaction.created_at)).all()
        
        report_data = [{
            "date": str(r.date),
            "total_sales": float(r.total_sales or 0),
            "transaction_count": r.transaction_count,
            "total_quantity": r.total_quantity
        } for r in results]
        
    elif group_by == "drug":
        # Group by drug
        results = db.query(
            models.Drug.brand_name,
            models.Drug.generic_name,
            func.sum(models.StockTransaction.total_price).label("total_sales"),
            func.count(models.StockTransaction.id).label("transaction_count"),
            func.sum(models.StockTransaction.quantity).label("total_quantity")
        ).join(
            models.Inventory, models.StockTransaction.inventory_id == models.Inventory.id
        ).join(
            models.Drug, models.Inventory.drug_id == models.Drug.id
        ).filter(
            models.StockTransaction.transaction_type == "sale",
            models.StockTransaction.created_at >= start,
            models.StockTransaction.created_at <= end
        ).group_by(models.Drug.id).all()
        
        report_data = [{
            "drug_name": r.brand_name,
            "generic_name": r.generic_name,
            "total_sales": float(r.total_sales or 0),
            "transaction_count": r.transaction_count,
            "total_quantity": r.total_quantity
        } for r in results]
    
    # Calculate totals
    total_sales = sum(item["total_sales"] for item in report_data)
    total_transactions = sum(item["transaction_count"] for item in report_data)
    total_quantity = sum(item["total_quantity"] for item in report_data)
    
    return {
        "report_type": "sales",
        "period": {
            "start_date": start_date,
            "end_date": end_date
        },
        "group_by": group_by,
        "summary": {
            "total_sales": total_sales,
            "total_transactions": total_transactions,
            "total_quantity": total_quantity
        },
        "data": report_data
    }

@router.get("/reports/inventory-value", response_model=dict)
def get_inventory_value_report(db: Session = Depends(get_db)):
    """Get inventory value report"""
    inventory_items = db.query(models.Inventory).filter(
        models.Inventory.quantity > 0
    ).all()
    
    total_cost_value = 0
    total_selling_value = 0
    
    for item in inventory_items:
        total_cost_value += item.quantity * item.unit_price
        total_selling_value += item.quantity * item.selling_price
    
    return {
        "report_type": "inventory_value",
        "total_items": len(inventory_items),
        "total_quantity": sum(item.quantity for item in inventory_items),
        "cost_value": total_cost_value,
        "selling_value": total_selling_value,
        "potential_profit": total_selling_value - total_cost_value,
        "items": [{
            "drug_name": item.drug.brand_name if item.drug else "Unknown",
            "quantity": item.quantity,
            "unit_cost": item.unit_price,
            "unit_selling": item.selling_price,
            "total_cost": item.quantity * item.unit_price,
            "total_selling": item.quantity * item.selling_price
        } for item in inventory_items]
    }

@router.get("/reports/prescription-stats", response_model=dict)
def get_prescription_stats(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get prescription statistics"""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    # Total prescriptions
    total_prescriptions = db.query(models.Prescription).filter(
        models.Prescription.date_prescribed >= cutoff_date
    ).count()
    
    # Prescriptions by status
    status_counts = db.query(
        models.Prescription.status,
        func.count(models.Prescription.id).label("count")
    ).filter(
        models.Prescription.date_prescribed >= cutoff_date
    ).group_by(models.Prescription.status).all()
    
    # Top prescribed drugs
    top_drugs = db.query(
        models.Drug.brand_name,
        models.Drug.generic_name,
        func.sum(models.PrescriptionItem.quantity).label("total_quantity"),
        func.count(models.PrescriptionItem.id).label("prescription_count")
    ).join(
        models.PrescriptionItem, models.PrescriptionItem.drug_id == models.Drug.id
    ).join(
        models.Prescription, models.PrescriptionItem.prescription_id == models.Prescription.id
    ).filter(
        models.Prescription.date_prescribed >= cutoff_date
    ).group_by(models.Drug.id).order_by(
        func.sum(models.PrescriptionItem.quantity).desc()
    ).limit(10).all()
    
    return {
        "period_days": days,
        "total_prescriptions": total_prescriptions,
        "status_distribution": {status: count for status, count in status_counts},
        "top_prescribed_drugs": [{
            "brand_name": drug.brand_name,
            "generic_name": drug.generic_name,
            "total_quantity": quantity,
            "prescription_count": count
        } for drug, generic, quantity, count in top_drugs]
    }
