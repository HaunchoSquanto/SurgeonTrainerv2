"""
Knee Surgical research case model (comprehensive)
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime


class RcKneeScope(SQLModel, table=True):
    """Knee surgical research data - covers ACL, HTO, meniscal, cartilage procedures"""
    __tablename__ = "rc_kneescope"
    
    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Foreign Key
    encounter_id: int = Field(foreign_key="encounter.id", index=True, unique=True)
    
    # Core Case Metadata
    fellow_or_pa: Optional[str] = Field(default=None, max_length=100)
    attending: Optional[str] = Field(default=None, max_length=100)
    mrn: Optional[str] = Field(default=None, max_length=50)
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    dob: Optional[date] = Field(default=None)
    surgery_date: Optional[date] = Field(default=None)
    laterality: Optional[str] = Field(default=None, max_length=20, description="Right/Left")
    procedure_type: Optional[str] = Field(default=None, max_length=50, description="Primary/Revision")
    
    # Intra-op Complications
    intraop_complications_present: Optional[bool] = Field(default=None)
    intraop_complications_explanation: Optional[str] = Field(default=None)
    just_meniscectomy_done: Optional[bool] = Field(default=None)
    other_procedure_not_listed: Optional[bool] = Field(default=None)
    other_procedure_list: Optional[str] = Field(default=None)
    ready_to_end_survey: Optional[bool] = Field(default=None)
    
    # Procedures Done (High-level Checkboxes)
    acl_done: Optional[bool] = Field(default=None)
    hto_done: Optional[bool] = Field(default=None, description="High tibial osteotomy")
    plc_done: Optional[bool] = Field(default=None, description="Posterolateral corner")
    meniscal_root_repair_done: Optional[bool] = Field(default=None)
    meniscal_repair_non_root_done: Optional[bool] = Field(default=None)
    meniscal_allograft_done: Optional[bool] = Field(default=None)
    meniscal_transplant_done: Optional[bool] = Field(default=None)
    patellar_instability_procedure_done: Optional[bool] = Field(default=None)
    cartilage_procedure_beyond_microfracture_done: Optional[bool] = Field(default=None)
    multiligament_repair_done: Optional[bool] = Field(default=None)
    patellofemoral_arthroplasty_done: Optional[bool] = Field(default=None)
    condyle_arthrosurface_done: Optional[bool] = Field(default=None)
    subchondroplasty_done: Optional[bool] = Field(default=None)
    peripatellar_release_done: Optional[bool] = Field(default=None)
    
    # Meniscus Repair Metadata
    medial_or_lateral_meniscus_repair: Optional[str] = Field(default=None, max_length=50, description="medial/lateral/both")
    
    # ACL DETAILS
    acl_autograft: Optional[bool] = Field(default=None)
    acl_allograft: Optional[bool] = Field(default=None)
    acl_hs_graft: Optional[bool] = Field(default=None, description="Hamstring")
    acl_quad_graft: Optional[bool] = Field(default=None, description="Quadriceps")
    acl_btb_graft: Optional[bool] = Field(default=None, description="Bone-tendon-bone")
    acl_block_graft: Optional[bool] = Field(default=None)
    acl_local_graft: Optional[bool] = Field(default=None)
    acl_internal_brace_used: Optional[bool] = Field(default=None)
    
    acl_concomitant_procedures_present: Optional[bool] = Field(default=None)
    acl_partial_medial_meniscectomy: Optional[bool] = Field(default=None)
    acl_partial_lateral_meniscectomy: Optional[bool] = Field(default=None)
    acl_medial_meniscus_repair: Optional[bool] = Field(default=None, description="MMR")
    acl_lateral_meniscus_repair: Optional[bool] = Field(default=None, description="LMR")
    
    acl_graftlink_used: Optional[bool] = Field(default=None)
    acl_graftlink_details: Optional[str] = Field(default=None, max_length=255)
    acl_st_gracilis_configuration: Optional[str] = Field(default=None, max_length=100)
    acl_graft_diameter_mm: Optional[float] = Field(default=None)
    acl_tibialtunnel_technique: Optional[str] = Field(default=None, max_length=100)
    acl_femoraltunnel_technique: Optional[str] = Field(default=None, max_length=100)
    
    # HTO DETAILS
    hto_valgus_producing: Optional[bool] = Field(default=None)
    hto_varus_producing: Optional[bool] = Field(default=None)
    hto_distal_femoral_varus_osteotomy: Optional[bool] = Field(default=None)
    hto_opposite_cortical_fractures_present: Optional[bool] = Field(default=None)
    
    hto_concomitant_meniscal_repair: Optional[bool] = Field(default=None)
    hto_concomitant_meniscal_allograft: Optional[bool] = Field(default=None)
    hto_concomitant_cartilage_restoration: Optional[bool] = Field(default=None)
    hto_concomitant_acl_reconstruction: Optional[bool] = Field(default=None)
    hto_concomitant_oc_allograft: Optional[bool] = Field(default=None)
    hto_concomitant_microfracture_abrasion: Optional[bool] = Field(default=None)
    
    hto_graft_used: Optional[str] = Field(default=None, max_length=255)
    hto_device_used: Optional[str] = Field(default=None, max_length=100)
    hto_cartilage_restoration_details: Optional[str] = Field(default=None)
    hto_degree_of_correction: Optional[float] = Field(default=None)
    hto_osteotomy_location: Optional[str] = Field(default=None, max_length=100)
    hto_opposite_cortical_fracture_treatment: Optional[str] = Field(default=None, max_length=255)
    
    # POSTEROLATERAL CORNER DETAILS
    plc_fibula_based_arciero: Optional[bool] = Field(default=None)
    plc_transtibial_laprade: Optional[bool] = Field(default=None)
    plc_acute: Optional[bool] = Field(default=None)
    plc_chronic: Optional[bool] = Field(default=None)
    plc_graft_used: Optional[str] = Field(default=None, max_length=100)
    plc_peroneal_nerve_identified: Optional[bool] = Field(default=None)
    plc_peroneal_nerve_released: Optional[bool] = Field(default=None)
    plc_graft_diameter_mm: Optional[float] = Field(default=None)
    plc_graft_type: Optional[str] = Field(default=None, max_length=50, description="Semi T/AT/PT")
    plc_fixation_method: Optional[str] = Field(default=None, max_length=100)
    
    # MENISCAL ROOT REPAIR DETAILS
    root_anchor_used: Optional[bool] = Field(default=None)
    root_transtibial: Optional[bool] = Field(default=None)
    root_acute: Optional[bool] = Field(default=None)
    root_mcl_pie_crusting_done: Optional[bool] = Field(default=None)
    root_preop_aware: Optional[bool] = Field(default=None)
    root_surprise_finding: Optional[bool] = Field(default=None)
    
    root_medial: Optional[bool] = Field(default=None)
    root_lateral: Optional[bool] = Field(default=None)
    root_tissue_quality: Optional[str] = Field(default=None, max_length=50)
    
    mfc_chondromalacia_grade: Optional[str] = Field(default=None, max_length=20)
    lfc_chondromalacia_grade: Optional[str] = Field(default=None, max_length=20)
    mtp_chondromalacia_grade: Optional[str] = Field(default=None, max_length=20)
    ltp_chondromalacia_grade: Optional[str] = Field(default=None, max_length=20)
    
    meniscus_tear_type: Optional[str] = Field(default=None, max_length=100)
    meniscus_num_sutures_used: Optional[int] = Field(default=None)
    meniscus_suture_configuration: Optional[str] = Field(default=None, max_length=100)
    
    # MENISCAL REPAIR (NON-ROOT)
    meniscal_all_inside: Optional[bool] = Field(default=None)
    meniscal_outside_in: Optional[bool] = Field(default=None)
    meniscal_inside_out: Optional[bool] = Field(default=None)
    meniscal_prp_or_biologic_used: Optional[bool] = Field(default=None)
    meniscal_augments_done_for_healing: Optional[bool] = Field(default=None)
    meniscal_repair_num_anchors: Optional[int] = Field(default=None)
    meniscal_repair_brand_suture: Optional[str] = Field(default=None, max_length=100)
    meniscal_repair_augment_details: Optional[str] = Field(default=None)
    
    meniscal_transplant_details: Optional[str] = Field(default=None)
    meniscal_remnant_tissue_remaining: Optional[str] = Field(default=None)
    
    # PATELLAR INSTABILITY
    pi_autograft: Optional[bool] = Field(default=None)
    pi_allograft: Optional[bool] = Field(default=None)
    pi_loose_body: Optional[bool] = Field(default=None)
    pi_chondral_defect: Optional[bool] = Field(default=None)
    pi_osteochondral_defect: Optional[bool] = Field(default=None)
    pi_lateral_tilt: Optional[bool] = Field(default=None)
    pi_lateral_release_done: Optional[bool] = Field(default=None)
    pi_patella_alta: Optional[bool] = Field(default=None)
    pi_trochlea_dysplasia: Optional[bool] = Field(default=None)
    pi_patella_anchor: Optional[bool] = Field(default=None)
    pi_tto_done: Optional[bool] = Field(default=None)
    pi_tto_details: Optional[str] = Field(default=None)
    pi_mqtfl_mpfl: Optional[str] = Field(default=None, max_length=100)
    pi_tt_tg: Optional[float] = Field(default=None)
    pi_femoral_fixation: Optional[str] = Field(default=None, max_length=100)
    
    # CARTILAGE PROCEDURES
    cp_oats_done: Optional[bool] = Field(default=None)
    cp_biocartilage_done: Optional[bool] = Field(default=None)
    cp_cartiform_done: Optional[bool] = Field(default=None)
    cp_maci_done: Optional[bool] = Field(default=None)
    cp_microfracture_done: Optional[bool] = Field(default=None)
    cp_chondroplasty_done: Optional[bool] = Field(default=None)
    
    cp_oats_autograft: Optional[bool] = Field(default=None)
    cp_cartiform_num_anchors: Optional[int] = Field(default=None)
    cp_graft_source: Optional[str] = Field(default=None, max_length=255)
    cp_core_measurements_patella: Optional[bool] = Field(default=None)
    cp_hemicondyle_source: Optional[str] = Field(default=None, max_length=100)
    cp_microfracture_details: Optional[str] = Field(default=None)
    cp_microfracture_subchondral_quality: Optional[str] = Field(default=None, max_length=100)
    cp_defect_size_mm: Optional[float] = Field(default=None)
    cp_defect_location: Optional[str] = Field(default=None, max_length=255)
    cp_technique: Optional[str] = Field(default=None, max_length=255)
    cp_structures_repaired: Optional[str] = Field(default=None)
    multiligament_repair_graft_used: Optional[str] = Field(default=None, max_length=255)
    
    # PATELLOFEMORAL ARTHROPLASTY
    pfa_lateral_facetectomy: Optional[bool] = Field(default=None)
    pfa_lateral_release: Optional[bool] = Field(default=None)
    pfa_mqpfl: Optional[bool] = Field(default=None)
    pfa_medial_capsule_imbrication: Optional[bool] = Field(default=None)
    pfa_ttt_done: Optional[bool] = Field(default=None)
    pfa_ttt_dimensions: Optional[str] = Field(default=None, max_length=100)
    pfa_scope_done: Optional[bool] = Field(default=None)
    pfa_scope_details: Optional[str] = Field(default=None)
    
    # CONDYLE ARTHROSURFACE DETAILS
    condyle_arthrosurface_size: Optional[str] = Field(default=None, max_length=50)
    condyle_arthrosurface_dimensions: Optional[str] = Field(default=None, max_length=100)
    condyle_augment_used: Optional[bool] = Field(default=None)
    condyle_augment_with_bone_graft: Optional[bool] = Field(default=None)
    condyle_augment_with_cement: Optional[bool] = Field(default=None)
    condyle_meniscus_condition_compartment: Optional[str] = Field(default=None, max_length=255)
    condyle_tibial_cartilage_icrs_grade: Optional[str] = Field(default=None, max_length=50)
    condyle_concomitant_meniscus_repair: Optional[bool] = Field(default=None)
    condyle_concomitant_partial_meniscectomy: Optional[bool] = Field(default=None)
    condyle_concomitant_pf_work: Optional[bool] = Field(default=None)
    condyle_concomitant_other: Optional[bool] = Field(default=None)
    condyle_concomitant_other_details: Optional[str] = Field(default=None)
    
    # SUBCHONDROPLASTY
    scp_location_mfc: Optional[bool] = Field(default=None)
    scp_location_lfc: Optional[bool] = Field(default=None)
    scp_location_mtp: Optional[bool] = Field(default=None)
    scp_location_ltp: Optional[bool] = Field(default=None)
    scp_lesion_size_mm: Optional[str] = Field(default=None, max_length=100)
    scp_amount_per_lesion_cc: Optional[str] = Field(default=None, max_length=100)
    scp_concomitant_ppr: Optional[bool] = Field(default=None)
    scp_concomitant_pm: Optional[bool] = Field(default=None)
    scp_concomitant_meniscus_repair: Optional[bool] = Field(default=None)
    scp_concomitant_other: Optional[bool] = Field(default=None)
    scp_concomitant_other_details: Optional[str] = Field(default=None)
    
    # PERIPATELLAR RELEASE INDICATIONS
    ppr_indication_postsurgical_traumatic_scar: Optional[bool] = Field(default=None)
    ppr_indication_pf_arthritis: Optional[bool] = Field(default=None)
    ppr_indication_tissue_balancing: Optional[bool] = Field(default=None)
    ppr_indication_patellar_stabilization: Optional[bool] = Field(default=None)
    
    # System Fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
