
# ==================== PHARMACY MODELS ====================

class Drug(Base):
    __tablename__ = "drugs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    drug_code = Column(String(50), unique=True, nullable=False, index=True)
    brand_name = Column(String(200), nullable=False)
    generic_name = Column(String(200), nullable=False)
    manufacturer = Column(String(200))
    drug_type = Column(String(50))  # tablet, capsule, syrup, injection, etc.
    strength = Column(String(100))  # e.g., "500mg", "10mg/ml"
    unit = Column(String(50))  # tablet, ml, mg, etc.
    category = Column(String(100))  # antibiotic, analgesic, antihypertensive, etc.
    prescription_required = Column(Boolean, default=True)
    schedule = Column(String(10))  # Schedule II, III, IV (for controlled substances)
    storage_conditions = Column(Text)  # JSON as string
    side_effects = Column(Text)  # JSON as string
    contraindications = Column(Text)  # JSON as string
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    inventory = relationship("Inventory", back_populates="drug", uselist=False)
    prescription_items = relationship("PrescriptionItem", back_populates="drug")
    drug_interactions = relationship("DrugInteraction", foreign_keys="[DrugInteraction.drug1_id]", back_populates="drug1")
    drug_interactions2 = relationship("DrugInteraction", foreign_keys="[DrugInteraction.drug2_id]", back_populates="drug2")
    
    def to_dict(self):
        return {
            "id": self.id,
            "drug_code": self.drug_code,
            "brand_name": self.brand_name,
            "generic_name": self.generic_name,
            "manufacturer": self.manufacturer,
            "drug_type": self.drug_type,
            "strength": self.strength,
            "unit": self.unit,
            "category": self.category,
            "prescription_required": self.prescription_required,
            "schedule": self.schedule,
            "storage_conditions": json.loads(self.storage_conditions) if self.storage_conditions else {},
            "side_effects": json.loads(self.side_effects) if self.side_effects else [],
            "contraindications": json.loads(self.contraindications) if self.contraindications else [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "is_active": self.is_active,
            "inventory": self.inventory.to_dict() if self.inventory else None
        }

class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    drug_id = Column(String(36), ForeignKey("drugs.id"), unique=True, nullable=False)
    batch_number = Column(String(100), nullable=False)
    quantity = Column(Integer, default=0)
    reorder_level = Column(Integer, default=10)
    reorder_quantity = Column(Integer, default=100)
    unit_price = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)
    expiry_date = Column(DateTime, nullable=False)
    supplier_id = Column(String(36), ForeignKey("suppliers.id"))
    location = Column(String(100))  # Shelf A1, Refrigerator, etc.
    last_restocked = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    drug = relationship("Drug", back_populates="inventory")
    supplier = relationship("Supplier", back_populates="inventory_items")
    stock_transactions = relationship("StockTransaction", back_populates="inventory")
    
    def to_dict(self):
        return {
            "id": self.id,
            "drug_id": self.drug_id,
            "batch_number": self.batch_number,
            "quantity": self.quantity,
            "reorder_level": self.reorder_level,
            "reorder_quantity": self.reorder_quantity,
            "unit_price": self.unit_price,
            "selling_price": self.selling_price,
            "expiry_date": self.expiry_date.isoformat() if self.expiry_date else None,
            "supplier_id": self.supplier_id,
            "location": self.location,
            "last_restocked": self.last_restocked.isoformat() if self.last_restocked else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "status": self.get_status(),
            "drug_info": {
                "brand_name": self.drug.brand_name if self.drug else None,
                "generic_name": self.drug.generic_name if self.drug else None,
                "strength": self.drug.strength if self.drug else None
            } if self.drug else None
        }
    
    def get_status(self):
        if self.quantity <= 0:
            return "out_of_stock"
        elif self.quantity <= self.reorder_level:
            return "low_stock"
        elif self.expiry_date and self.expiry_date < datetime.utcnow():
            return "expired"
        else:
            return "in_stock"

class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    supplier_code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    contact_person = Column(String(200))
    email = Column(String(200))
    phone = Column(String(20))
    address = Column(Text)  # JSON as string
    tax_id = Column(String(50))
    payment_terms = Column(String(100))
    delivery_time = Column(Integer)  # in days
    rating = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    inventory_items = relationship("Inventory", back_populates="supplier")
    purchase_orders = relationship("PurchaseOrder", back_populates="supplier")
    
    def to_dict(self):
        return {
            "id": self.id,
            "supplier_code": self.supplier_code,
            "name": self.name,
            "contact_person": self.contact_person,
            "email": self.email,
            "phone": self.phone,
            "address": json.loads(self.address) if self.address else {},
            "tax_id": self.tax_id,
            "payment_terms": self.payment_terms,
            "delivery_time": self.delivery_time,
            "rating": self.rating,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    po_number = Column(String(50), unique=True, nullable=False, index=True)
    supplier_id = Column(String(36), ForeignKey("suppliers.id"), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    expected_delivery = Column(DateTime)
    status = Column(String(20), default="pending")  # pending, approved, ordered, delivered, cancelled
    total_amount = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    grand_total = Column(Float, default=0.0)
    notes = Column(Text)
    created_by = Column(String(100))
    approved_by = Column(String(100))
    approved_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    supplier = relationship("Supplier", back_populates="purchase_orders")
    po_items = relationship("PurchaseOrderItem", back_populates="purchase_order")
    
    def to_dict(self):
        return {
            "id": self.id,
            "po_number": self.po_number,
            "supplier_id": self.supplier_id,
            "order_date": self.order_date.isoformat() if self.order_date else None,
            "expected_delivery": self.expected_delivery.isoformat() if self.expected_delivery else None,
            "status": self.status,
            "total_amount": self.total_amount,
            "tax_amount": self.tax_amount,
            "discount_amount": self.discount_amount,
            "grand_total": self.grand_total,
            "notes": self.notes,
            "created_by": self.created_by,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "supplier_name": self.supplier.name if self.supplier else None,
            "items_count": len(self.po_items) if self.po_items else 0
        }

class PurchaseOrderItem(Base):
    __tablename__ = "purchase_order_items"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    purchase_order_id = Column(String(36), ForeignKey("purchase_orders.id"), nullable=False)
    drug_id = Column(String(36), ForeignKey("drugs.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    received_quantity = Column(Integer, default=0)
    status = Column(String(20), default="pending")  # pending, partially_received, received
    notes = Column(Text)
    
    # Relationships
    purchase_order = relationship("PurchaseOrder", back_populates="po_items")
    drug = relationship("Drug")
    
    def to_dict(self):
        return {
            "id": self.id,
            "purchase_order_id": self.purchase_order_id,
            "drug_id": self.drug_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total_price": self.total_price,
            "received_quantity": self.received_quantity,
            "status": self.status,
            "notes": self.notes,
            "drug_name": self.drug.brand_name if self.drug else None,
            "generic_name": self.drug.generic_name if self.drug else None
        }

class StockTransaction(Base):
    __tablename__ = "stock_transactions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    transaction_id = Column(String(50), unique=True, nullable=False, index=True)
    inventory_id = Column(String(36), ForeignKey("inventory.id"), nullable=False)
    transaction_type = Column(String(20), nullable=False)  # purchase, sale, return, adjustment, transfer
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    reference_id = Column(String(100))  # PO number, prescription ID, etc.
    reference_type = Column(String(50))  # purchase_order, prescription, adjustment
    notes = Column(Text)
    created_by = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    inventory = relationship("Inventory", back_populates="stock_transactions")
    
    def to_dict(self):
        return {
            "id": self.id,
            "transaction_id": self.transaction_id,
            "inventory_id": self.inventory_id,
            "transaction_type": self.transaction_type,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total_price": self.total_price,
            "reference_id": self.reference_id,
            "reference_type": self.reference_type,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "drug_name": self.inventory.drug.brand_name if self.inventory and self.inventory.drug else None
        }

class DrugInteraction(Base):
    __tablename__ = "drug_interactions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    drug1_id = Column(String(36), ForeignKey("drugs.id"), nullable=False)
    drug2_id = Column(String(36), ForeignKey("drugs.id"), nullable=False)
    severity = Column(String(20))  # minor, moderate, major, contraindicated
    description = Column(Text)
    mechanism = Column(Text)
    management = Column(Text)
    evidence_level = Column(String(50))  # established, probable, possible, unlikely
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    drug1 = relationship("Drug", foreign_keys=[drug1_id], back_populates="drug_interactions")
    drug2 = relationship("Drug", foreign_keys=[drug2_id], back_populates="drug_interactions2")
    
    def to_dict(self):
        return {
            "id": self.id,
            "drug1_id": self.drug1_id,
            "drug2_id": self.drug2_id,
            "severity": self.severity,
            "description": self.description,
            "mechanism": self.mechanism,
            "management": self.management,
            "evidence_level": self.evidence_level,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "drug1_name": self.drug1.brand_name if self.drug1 else None,
            "drug2_name": self.drug2.brand_name if self.drug2 else None
        }

# Update the Prescription model to link with pharmacy
class PrescriptionItem(Base):
    __tablename__ = "prescription_items"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    prescription_id = Column(String(36), ForeignKey("prescriptions.id"), nullable=False)
    drug_id = Column(String(36), ForeignKey("drugs.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    dosage = Column(String(100))
    frequency = Column(String(100))
    duration = Column(String(100))
    instructions = Column(Text)
    status = Column(String(20), default="pending")  # pending, dispensed, cancelled
    dispensed_by = Column(String(100))
    dispensed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    prescription = relationship("Prescription", back_populates="items")
    drug = relationship("Drug", back_populates="prescription_items")
    
    def to_dict(self):
        return {
            "id": self.id,
            "prescription_id": self.prescription_id,
            "drug_id": self.drug_id,
            "quantity": self.quantity,
            "dosage": self.dosage,
            "frequency": self.frequency,
            "duration": self.duration,
            "instructions": self.instructions,
            "status": self.status,
            "dispensed_by": self.dispensed_by,
            "dispensed_at": self.dispensed_at.isoformat() if self.dispensed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "drug_info": {
                "brand_name": self.drug.brand_name if self.drug else None,
                "generic_name": self.drug.generic_name if self.drug else None,
                "strength": self.drug.strength if self.drug else None
            } if self.drug else None
        }

# Update the Prescription model to include items
class Prescription(Base):
    __tablename__ = "prescriptions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    prescription_number = Column(String(50), unique=True, nullable=False, index=True)
    patient_id = Column(String(36), ForeignKey("patients.id"))
    doctor_id = Column(String(36), ForeignKey("doctors.id"))
    date_prescribed = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="active")  # active, dispensed, expired, cancelled
    validity_days = Column(Integer, default=30)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient", back_populates="prescriptions")
    doctor = relationship("Doctor", back_populates="prescriptions")
    items = relationship("PrescriptionItem", back_populates="prescription")
    
    def to_dict(self):
        return {
            "id": self.id,
            "prescription_number": self.prescription_number,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "date_prescribed": self.date_prescribed.isoformat() if self.date_prescribed else None,
            "status": self.status,
            "validity_days": self.validity_days,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "patient_name": f"{self.patient.first_name} {self.patient.last_name}" if self.patient else None,
            "doctor_name": f"Dr. {self.doctor.first_name} {self.doctor.last_name}" if self.doctor else None,
            "items": [item.to_dict() for item in self.items] if self.items else []
        }
