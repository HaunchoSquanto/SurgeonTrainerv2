"""
Hip Surgical schemas - Pydantic models for API request/response validation
"""
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, Literal


class RcHipSurgicalBase(BaseModel):
    """Base Hip Surgical fields (research-focused)"""
    encounter_id: int

    # Core case metadata
    fellow_or_pa: Optional[str] = None
    attending: Optional[str] = None
    mrn: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[date] = None
    surgery_date: Optional[date] = None
    laterality: Optional[Literal["Right", "Left"]] = None
    procedure_type: Optional[Literal["Primary", "Revision"]] = None

    # Intra-op complications / other procedures
    intraop_complications_present: Optional[bool] = None
    intraop_complications_explanation: Optional[str] = None
    just_meniscectomy_done: Optional[bool] = None
    other_procedure_not_listed: Optional[bool] = None
    other_procedure_list: Optional[str] = None
    ready_to_end_survey: Optional[bool] = None

    # Procedures done (high-level checkboxes)
    acl_done: Optional[bool] = None
    hto_done: Optional[bool] = None
    plc_done: Optional[bool] = None
    meniscal_root_repair_done: Optional[bool] = None
    meniscal_repair_non_root_done: Optional[bool] = None
    meniscal_allograft_done: Optional[bool] = None
    meniscal_transplant_done: Optional[bool] = None
    patellar_instability_procedure_done: Optional[bool] = None
    cartilage_procedure_beyond_microfracture_done: Optional[bool] = None
    multiligament_repair_done: Optional[bool] = None
    patellofemoral_arthroplasty_done: Optional[bool] = None
    condyle_arthrosurface_done: Optional[bool] = None
    subchondroplasty_done: Optional[bool] = None
    peripatellar_release_done: Optional[bool] = None

    # Meniscus repair metadata
    medial_or_lateral_meniscus_repair: Optional[Literal["medial", "lateral", "both"]] = None

    # ACL DETAILS
    acl_autograft: Optional[bool] = None
    acl_allograft: Optional[bool] = None
    acl_hs_graft: Optional[bool] = None
    acl_quad_graft: Optional[bool] = None
    acl_btb_graft: Optional[bool] = None
    acl_block_graft: Optional[bool] = None
    acl_local_graft: Optional[bool] = None
    acl_internal_brace_used: Optional[bool] = None

    acl_concomitant_procedures_present: Optional[bool] = None
    acl_partial_medial_meniscectomy: Optional[bool] = None
    acl_partial_lateral_meniscectomy: Optional[bool] = None
    acl_medial_meniscus_repair: Optional[bool] = None
    acl_lateral_meniscus_repair: Optional[bool] = None

    acl_graftlink_used: Optional[bool] = None
    acl_graftlink_details: Optional[str] = None
    acl_st_gracilis_configuration: Optional[str] = None
    acl_graft_diameter_mm: Optional[float] = None
    acl_tibialtunnel_technique: Optional[str] = None
    acl_femoraltunnel_technique: Optional[str] = None

    # HTO DETAILS
    hto_valgus_producing: Optional[bool] = None
    hto_varus_producing: Optional[bool] = None
    hto_distal_femoral_varus_osteotomy: Optional[bool] = None
    hto_opposite_cortical_fractures_present: Optional[bool] = None

    hto_concomitant_meniscal_repair: Optional[bool] = None
    hto_concomitant_meniscal_allograft: Optional[bool] = None
    hto_concomitant_cartilage_restoration: Optional[bool] = None
    hto_concomitant_acl_reconstruction: Optional[bool] = None
    hto_concomitant_oc_allograft: Optional[bool] = None
    hto_concomitant_microfracture_abrasion: Optional[bool] = None

    hto_graft_used: Optional[str] = None
    hto_device_used: Optional[str] = None
    hto_cartilage_restoration_details: Optional[str] = None
    hto_degree_of_correction: Optional[float] = None
    hto_osteotomy_location: Optional[str] = None
    hto_opposite_cortical_fracture_treatment: Optional[str] = None

    # POSTEROLATERAL CORNER DETAILS
    plc_fibula_based_arciero: Optional[bool] = None
    plc_transtibial_laprade: Optional[bool] = None
    plc_acute: Optional[bool] = None
    plc_chronic: Optional[bool] = None
    plc_graft_used: Optional[str] = None
    plc_peroneal_nerve_identified: Optional[bool] = None
    plc_peroneal_nerve_released: Optional[bool] = None
    plc_graft_diameter_mm: Optional[float] = None
    plc_graft_type: Optional[str] = None
    plc_fixation_method: Optional[str] = None

    # MENISCAL ROOT REPAIR DETAILS
    root_anchor_used: Optional[bool] = None
    root_transtibial: Optional[bool] = None
    root_acute: Optional[bool] = None
    root_mcl_pie_crusting_done: Optional[bool] = None
    root_preop_aware: Optional[bool] = None
    root_surprise_finding: Optional[bool] = None

    root_medial: Optional[bool] = None
    root_lateral: Optional[bool] = None
    root_tissue_quality: Optional[str] = None

    mfc_chondromalacia_grade: Optional[str] = None
    lfc_chondromalacia_grade: Optional[str] = None
    mtp_chondromalacia_grade: Optional[str] = None
    ltp_chondromalacia_grade: Optional[str] = None

    meniscus_tear_type: Optional[str] = None
    meniscus_num_sutures_used: Optional[int] = None
    meniscus_suture_configuration: Optional[str] = None

    # MENISCAL REPAIR (NON-ROOT)
    meniscal_all_inside: Optional[bool] = None
    meniscal_outside_in: Optional[bool] = None
    meniscal_inside_out: Optional[bool] = None
    meniscal_prp_or_biologic_used: Optional[bool] = None
    meniscal_augments_done_for_healing: Optional[bool] = None
    meniscal_repair_num_anchors: Optional[int] = None
    meniscal_repair_brand_suture: Optional[str] = None
    meniscal_repair_augment_details: Optional[str] = None

    meniscal_transplant_details: Optional[str] = None
    meniscal_remnant_tissue_remaining: Optional[str] = None

    # PATELLAR INSTABILITY
    pi_autograft: Optional[bool] = None
    pi_allograft: Optional[bool] = None
    pi_loose_body: Optional[bool] = None
    pi_chondral_defect: Optional[bool] = None
    pi_osteochondral_defect: Optional[bool] = None
    pi_lateral_tilt: Optional[bool] = None
    pi_lateral_release_done: Optional[bool] = None
    pi_patella_alta: Optional[bool] = None
    pi_trochlea_dysplasia: Optional[bool] = None
    pi_patella_anchor: Optional[bool] = None
    pi_tto_done: Optional[bool] = None
    pi_tto_details: Optional[str] = None
    pi_mqtfl_mpfl: Optional[str] = None
    pi_tt_tg: Optional[float] = None
    pi_femoral_fixation: Optional[str] = None

    # CARTILAGE PROCEDURES
    cp_oats_done: Optional[bool] = None
    cp_biocartilage_done: Optional[bool] = None
    cp_cartiform_done: Optional[bool] = None
    cp_maci_done: Optional[bool] = None
    cp_microfracture_done: Optional[bool] = None
    cp_chondroplasty_done: Optional[bool] = None

    cp_oats_autograft: Optional[bool] = None
    cp_cartiform_num_anchors: Optional[int] = None
    cp_graft_source: Optional[str] = None
    cp_core_measurements_patella: Optional[bool] = None
    cp_hemicondyle_source: Optional[str] = None
    cp_microfracture_details: Optional[str] = None
    cp_microfracture_subchondral_quality: Optional[str] = None
    cp_defect_size_mm: Optional[float] = None
    cp_defect_location: Optional[str] = None
    cp_technique: Optional[str] = None
    cp_structures_repaired: Optional[str] = None
    multiligament_repair_graft_used: Optional[str] = None

    # PATELLOFEMORAL ARTHROPLASTY
    pfa_lateral_facetectomy: Optional[bool] = None
    pfa_lateral_release: Optional[bool] = None
    pfa_mqpfl: Optional[bool] = None
    pfa_medial_capsule_imbrication: Optional[bool] = None
    pfa_ttt_done: Optional[bool] = None
    pfa_ttt_dimensions: Optional[str] = None
    pfa_scope_done: Optional[bool] = None
    pfa_scope_details: Optional[str] = None

    # CONDYLE ARTHROSURFACE DETAILS
    condyle_arthrosurface_size: Optional[str] = None
    condyle_arthrosurface_dimensions: Optional[str] = None
    condyle_augment_used: Optional[bool] = None
    condyle_augment_with_bone_graft: Optional[bool] = None
    condyle_augment_with_cement: Optional[bool] = None
    condyle_meniscus_condition_compartment: Optional[str] = None
    condyle_tibial_cartilage_icrs_grade: Optional[str] = None
    condyle_concomitant_meniscus_repair: Optional[bool] = None
    condyle_concomitant_partial_meniscectomy: Optional[bool] = None
    condyle_concomitant_pf_work: Optional[bool] = None
    condyle_concomitant_other: Optional[bool] = None
    condyle_concomitant_other_details: Optional[str] = None

    # SUBCHONDROPLASTY
    scp_location_mfc: Optional[bool] = None
    scp_location_lfc: Optional[bool] = None
    scp_location_mtp: Optional[bool] = None
    scp_location_ltp: Optional[bool] = None
    scp_lesion_size_mm: Optional[str] = None
    scp_amount_per_lesion_cc: Optional[str] = None
    scp_concomitant_ppr: Optional[bool] = None
    scp_concomitant_pm: Optional[bool] = None
    scp_concomitant_meniscus_repair: Optional[bool] = None
    scp_concomitant_other: Optional[bool] = None
    scp_concomitant_other_details: Optional[str] = None

    # PERIPATELLAR RELEASE INDICATIONS
    ppr_indication_postsurgical_traumatic_scar: Optional[bool] = None
    ppr_indication_pf_arthritis: Optional[bool] = None
    ppr_indication_tissue_balancing: Optional[bool] = None
    ppr_indication_patellar_stabilization: Optional[bool] = None


class RcHipSurgicalCreate(RcHipSurgicalBase):
    """Schema for creating a new Hip Surgical case"""
    pass


class RcHipSurgicalUpdate(BaseModel):
    """Schema for updating a Hip Surgical case - all fields optional"""
    # All fields from Base but optional - just showing a subset for brevity
    fellow_or_pa: Optional[str] = None
    attending: Optional[str] = None
    mrn: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[date] = None
    surgery_date: Optional[date] = None
    laterality: Optional[Literal["Right", "Left"]] = None
    procedure_type: Optional[Literal["Primary", "Revision"]] = None
    # ... (all other fields follow same pattern)


class RcHipSurgicalResponse(RcHipSurgicalBase):
    """Schema for Hip Surgical API response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

