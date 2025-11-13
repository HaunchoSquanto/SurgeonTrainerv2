"""Initial migration with patient management tables.

Revision ID: 001
Revises: 
Create Date: 2025-11-11 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create initial tables for patient management system."""
    
    # Create patients table
    op.create_table(
        'patients',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('mrn', sa.String(), nullable=False),
        sa.Column('external_id', sa.String(), nullable=True),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('middle_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('preferred_name', sa.String(), nullable=True),
        sa.Column('date_of_birth', sa.Date(), nullable=False),
        sa.Column('sex', sa.String(), nullable=False),
        sa.Column('gender_identity', sa.String(), nullable=True),
        sa.Column('pronouns', sa.String(), nullable=True),
        
        # Contact Information
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('phone_primary', sa.String(), nullable=True),
        sa.Column('phone_secondary', sa.String(), nullable=True),
        sa.Column('phone_emergency', sa.String(), nullable=True),
        
        # Address
        sa.Column('address_line1', sa.String(), nullable=True),
        sa.Column('address_line2', sa.String(), nullable=True),
        sa.Column('city', sa.String(), nullable=True),
        sa.Column('state', sa.String(), nullable=True),
        sa.Column('zip_code', sa.String(), nullable=True),
        sa.Column('country', sa.String(), nullable=False),
        
        # Personal Details
        sa.Column('marital_status', sa.String(), nullable=True),
        sa.Column('preferred_language', sa.String(), nullable=True),
        sa.Column('race', sa.String(), nullable=True),
        sa.Column('ethnicity', sa.String(), nullable=True),
        sa.Column('religion', sa.String(), nullable=True),
        
        # Emergency Contact
        sa.Column('emergency_contact_name', sa.String(), nullable=True),
        sa.Column('emergency_contact_relationship', sa.String(), nullable=True),
        sa.Column('emergency_contact_phone', sa.String(), nullable=True),
        sa.Column('emergency_contact_email', sa.String(), nullable=True),
        
        # Medical Information
        sa.Column('blood_type', sa.String(), nullable=True),
        sa.Column('height_cm', sa.Float(), nullable=True),
        sa.Column('weight_kg', sa.Float(), nullable=True),
        sa.Column('bmi', sa.Float(), nullable=True),
        
        # Primary Care
        sa.Column('primary_care_physician', sa.String(), nullable=True),
        sa.Column('primary_care_clinic', sa.String(), nullable=True),
        sa.Column('referring_physician', sa.String(), nullable=True),
        
        # Insurance Information
        sa.Column('insurance_primary_provider', sa.String(), nullable=True),
        sa.Column('insurance_primary_policy_number', sa.String(), nullable=True),
        sa.Column('insurance_primary_group_number', sa.String(), nullable=True),
        sa.Column('insurance_primary_type', sa.String(), nullable=True),
        sa.Column('insurance_secondary_provider', sa.String(), nullable=True),
        sa.Column('insurance_secondary_policy_number', sa.String(), nullable=True),
        sa.Column('insurance_secondary_group_number', sa.String(), nullable=True),
        sa.Column('insurance_secondary_type', sa.String(), nullable=True),
        
        # JSON fields for flexible storage
        sa.Column('allergies', sa.JSON(), nullable=True),
        sa.Column('medications', sa.JSON(), nullable=True),
        sa.Column('chronic_conditions', sa.JSON(), nullable=True),
        sa.Column('past_surgeries', sa.JSON(), nullable=True),
        sa.Column('family_history', sa.JSON(), nullable=True),
        sa.Column('social_history', sa.JSON(), nullable=True),
        
        # Clinical Notes
        sa.Column('chief_complaint', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        
        # Administrative
        sa.Column('patient_status', sa.String(), nullable=False),
        sa.Column('admission_date', sa.Date(), nullable=True),
        sa.Column('discharge_date', sa.Date(), nullable=True),
        sa.Column('deceased_date', sa.Date(), nullable=True),
        
        # Custom Fields
        sa.Column('custom_fields', sa.JSON(), nullable=True),
        
        # Metadata
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.Column('updated_by', sa.String(), nullable=True),
        
        # Soft delete
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('deleted_by', sa.String(), nullable=True),
        
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for patients table
    op.create_index(op.f('ix_patients_mrn'), 'patients', ['mrn'], unique=True)
    op.create_index(op.f('ix_patients_external_id'), 'patients', ['external_id'], unique=False)
    op.create_index(op.f('ix_patients_first_name'), 'patients', ['first_name'], unique=False)
    op.create_index(op.f('ix_patients_last_name'), 'patients', ['last_name'], unique=False)
    op.create_index(op.f('ix_patients_date_of_birth'), 'patients', ['date_of_birth'], unique=False)
    op.create_index(op.f('ix_patients_email'), 'patients', ['email'], unique=False)
    op.create_index(op.f('ix_patients_phone_primary'), 'patients', ['phone_primary'], unique=False)
    op.create_index(op.f('ix_patients_city'), 'patients', ['city'], unique=False)
    op.create_index(op.f('ix_patients_state'), 'patients', ['state'], unique=False)
    op.create_index(op.f('ix_patients_zip_code'), 'patients', ['zip_code'], unique=False)
    op.create_index(op.f('ix_patients_patient_status'), 'patients', ['patient_status'], unique=False)
    op.create_index(op.f('ix_patients_admission_date'), 'patients', ['admission_date'], unique=False)
    op.create_index(op.f('ix_patients_insurance_primary_type'), 'patients', ['insurance_primary_type'], unique=False)
    op.create_index(op.f('ix_patients_created_at'), 'patients', ['created_at'], unique=False)
    op.create_index(op.f('ix_patients_is_deleted'), 'patients', ['is_deleted'], unique=False)
    
    # Create patient_visits table
    op.create_table(
        'patient_visits',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('patient_id', sa.Integer(), nullable=False),
        sa.Column('case_id', sa.String(), nullable=True),
        sa.Column('visit_date', sa.Date(), nullable=False),
        sa.Column('visit_type', sa.String(), nullable=False),
        sa.Column('visit_reason', sa.String(), nullable=True),
        sa.Column('chief_complaint', sa.Text(), nullable=True),
        sa.Column('diagnosis', sa.String(), nullable=True),
        sa.Column('treatment_plan', sa.Text(), nullable=True),
        sa.Column('attending_physician', sa.String(), nullable=True),
        sa.Column('consulting_physicians', sa.String(), nullable=True),
        sa.Column('vital_signs', sa.JSON(), nullable=True),
        sa.Column('billing_codes', sa.JSON(), nullable=True),
        sa.Column('visit_cost', sa.Float(), nullable=True),
        sa.Column('visit_notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
    )
    
    op.create_index(op.f('ix_patient_visits_patient_id'), 'patient_visits', ['patient_id'], unique=False)
    op.create_index(op.f('ix_patient_visits_visit_date'), 'patient_visits', ['visit_date'], unique=False)
    op.create_index(op.f('ix_patient_visits_visit_type'), 'patient_visits', ['visit_type'], unique=False)
    
    # Create patient_documents table
    op.create_table(
        'patient_documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('patient_id', sa.Integer(), nullable=False),
        sa.Column('visit_id', sa.Integer(), nullable=True),
        sa.Column('document_type', sa.String(), nullable=False),
        sa.Column('document_title', sa.String(), nullable=False),
        sa.Column('document_description', sa.String(), nullable=True),
        sa.Column('file_path', sa.String(), nullable=True),
        sa.Column('file_url', sa.String(), nullable=True),
        sa.Column('file_size_bytes', sa.Integer(), nullable=True),
        sa.Column('mime_type', sa.String(), nullable=True),
        sa.Column('document_date', sa.Date(), nullable=True),
        sa.Column('document_category', sa.String(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('is_confidential', sa.Boolean(), nullable=False),
        sa.Column('access_level', sa.String(), nullable=True),
        sa.Column('uploaded_by', sa.String(), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(), nullable=False),
        
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
        sa.ForeignKeyConstraint(['visit_id'], ['patient_visits.id'], ),
    )
    
    op.create_index(op.f('ix_patient_documents_patient_id'), 'patient_documents', ['patient_id'], unique=False)
    op.create_index(op.f('ix_patient_documents_visit_id'), 'patient_documents', ['visit_id'], unique=False)
    op.create_index(op.f('ix_patient_documents_document_type'), 'patient_documents', ['document_type'], unique=False)
    op.create_index(op.f('ix_patient_documents_document_date'), 'patient_documents', ['document_date'], unique=False)
    op.create_index(op.f('ix_patient_documents_document_category'), 'patient_documents', ['document_category'], unique=False)
    op.create_index(op.f('ix_patient_documents_uploaded_at'), 'patient_documents', ['uploaded_at'], unique=False)


def downgrade() -> None:
    """Drop all patient management tables."""
    
    op.drop_index(op.f('ix_patient_documents_uploaded_at'), table_name='patient_documents')
    op.drop_index(op.f('ix_patient_documents_document_category'), table_name='patient_documents')
    op.drop_index(op.f('ix_patient_documents_document_date'), table_name='patient_documents')
    op.drop_index(op.f('ix_patient_documents_document_type'), table_name='patient_documents')
    op.drop_index(op.f('ix_patient_documents_visit_id'), table_name='patient_documents')
    op.drop_index(op.f('ix_patient_documents_patient_id'), table_name='patient_documents')
    op.drop_table('patient_documents')
    
    op.drop_index(op.f('ix_patient_visits_visit_type'), table_name='patient_visits')
    op.drop_index(op.f('ix_patient_visits_visit_date'), table_name='patient_visits')
    op.drop_index(op.f('ix_patient_visits_patient_id'), table_name='patient_visits')
    op.drop_table('patient_visits')
    
    op.drop_index(op.f('ix_patients_is_deleted'), table_name='patients')
    op.drop_index(op.f('ix_patients_created_at'), table_name='patients')
    op.drop_index(op.f('ix_patients_insurance_primary_type'), table_name='patients')
    op.drop_index(op.f('ix_patients_admission_date'), table_name='patients')
    op.drop_index(op.f('ix_patients_patient_status'), table_name='patients')
    op.drop_index(op.f('ix_patients_zip_code'), table_name='patients')
    op.drop_index(op.f('ix_patients_state'), table_name='patients')
    op.drop_index(op.f('ix_patients_city'), table_name='patients')
    op.drop_index(op.f('ix_patients_phone_primary'), table_name='patients')
    op.drop_index(op.f('ix_patients_email'), table_name='patients')
    op.drop_index(op.f('ix_patients_date_of_birth'), table_name='patients')
    op.drop_index(op.f('ix_patients_last_name'), table_name='patients')
    op.drop_index(op.f('ix_patients_first_name'), table_name='patients')
    op.drop_index(op.f('ix_patients_external_id'), table_name='patients')
    op.drop_index(op.f('ix_patients_mrn'), table_name='patients')
    op.drop_table('patients')
