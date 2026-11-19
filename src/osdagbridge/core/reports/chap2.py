# =============================================================================
# Chapter 2: Input Parameters
# Refactored to use centralized styles and LongTable with repeated headers.
# =============================================================================

from osdagbridge.core.utils.common import (
    KEY_CARRIAGEWAY_WIDTH,
    KEY_CB_LOAD,
    KEY_CB_TYPE,
    KEY_CROSS_BRACING,
    KEY_DECK_CONCRETE_GRADE_BASIC,
    KEY_DESIGN_MODE,
    KEY_DO_GAMMA_C_BASIC,
    KEY_DO_GAMMA_FLT,
    KEY_DO_GAMMA_M0,
    KEY_DO_GAMMA_M1,
    KEY_DO_GAMMA_MF,
    KEY_DO_GAMMA_S,
    KEY_DO_GAMMA_V,
    KEY_END_DIAPHRAGM,
    KEY_FOOTPATH,
    KEY_GIRDER,
    KEY_INCLUDE_MEDIAN,
    KEY_MD_TYPE,
    KEY_MP_CB_BRACING_SECTION_DESIGNATION,
    KEY_MP_CB_MEMBER_ID,
    KEY_MP_CB_SELECT_GIRDERS,
    KEY_MP_CB_SPACING,
    KEY_MP_CB_TYPE,
    KEY_MP_ED_BRACING_SECTION_DESIGNATION,
    KEY_MP_ED_MEMBER_ID,
    KEY_MP_ED_SELECT_GIRDERS,
    KEY_MP_ED_TYPE,
    KEY_MP_GD_MEMBER_ID,
    KEY_MP_GD_SELECT_GIRDER,
    KEY_MP_GIRDER_BOTTOM_FLANGE_THICKNESS,
    KEY_MP_GIRDER_BOTTOM_FLANGE_WIDTH,
    KEY_MP_GIRDER_DEPTH,
    KEY_MP_GIRDER_SYMMETRY,
    KEY_MP_GIRDER_TOP_FLANGE_THICKNESS,
    KEY_MP_GIRDER_TOP_FLANGE_WIDTH,
    KEY_MP_GIRDER_TORSIONAL_RESTRAINT,
    KEY_MP_GIRDER_TYPE,
    KEY_MP_GIRDER_WARPING_RESTRAINT,
    KEY_MP_GIRDER_WEB_THICKNESS,
    KEY_MP_GIRDER_WEB_TYPE,
    KEY_MP_STIFFENER_BEARING_THICKNESS,
    KEY_MP_STIFFENER_INTERMEDIATE,
    KEY_MP_STIFFENER_INTERMEDIATE_SPACING,
    KEY_MP_STIFFENER_INTERMEDIATE_THICKNESS,
    KEY_MP_STIFFENER_LONGITUDINAL,
    KEY_MP_STIFFENER_NO_BEARING_STIFFENERS,
    KEY_MP_STIFFENER_SPACING,
    KEY_RL_LOAD_VALUE,
    KEY_RL_TYPE,
    KEY_SD_SHEAR_DIAMETER,
    KEY_SD_SHEAR_HEIGHT,
    KEY_SD_SHEAR_STUDS_PER_SECTION,
    KEY_SD_SHEAR_ULTIMATE_STRENGTH,
    KEY_SD_SHEAR_YIELD_STRENGTH,
    KEY_SKEW_ANGLE,
    KEY_SPAN,
    KEY_STRUCTURE_TYPE,
    KEY_TS_DECK_OVERHANG,
    KEY_TS_DECK_THICKNESS,
    KEY_TS_FOOTPATH_WIDTH,
    KEY_TS_GIRDER_SPACING,
    KEY_TS_NO_OF_GIRDERS,
    KEY_TS_OVERALL_WIDTH,
    KEY_WC_LD_LANE_TABLE_COUNT,
    KEY_WC_MATERIAL,
    KEY_WC_THICKNESS
)

from osdagbridge.core.reports.report_utils import _render_value, get_girder_entries, _tex
from osdagbridge.core.reports.styles import make_longtable_header, make_longtable_footer, lt_block


def ch2_input_parameters(m, input_dict, output_dict=None):
    girder_entries = get_girder_entries(input_dict)
    n_girders = len(girder_entries)
    
    # Median row only shown when the user included a median
    median_row = ""
    if str(input_dict.get(KEY_INCLUDE_MEDIAN, "")).strip().lower() in ("yes", "true", "1"):
        median_row = (r"\textnormal{Median Type} & "
                      + _render_value(input_dict, KEY_MD_TYPE)
                      + r""" \\[6pt]
\hline
""")

    # 1. Project Location Table
    t_loc_body = rf"""
\textnormal{{Project Location}} & {_tex(m.project_location)} \\[6pt]
\hline
\textnormal{{Latitude / Longitude}} & {_render_value(input_dict, 'latitude')}, {_render_value(input_dict, 'longitude')} \\[6pt]
\hline
\textnormal{{Seismic Zone (IRC 6)}} & {_render_value(input_dict, 'seismic_zone')} \\[6pt]
\hline
\textnormal{{Basic Wind Speed (IRC 6)}} & {_render_value(input_dict, 'wind_speed', ' m/s')} \\[6pt]
\hline
\textnormal{{Shade Temp. Max / Min (IRC 6)}} & {_render_value(input_dict, 'shade_temp_max', '')} °C / {_render_value(input_dict, 'shade_temp_min', '')} °C \\[6pt]
"""
    t_loc = lt_block("Project Location", "|L{5.5cm}|L{9.5cm}|", r"\textbf{Parameter} & \textbf{Value}",
                     t_loc_body, label="subsec:project-location", num_cols=2)

    # 2. Bridge Geometry Table
    t_geom_body = rf"""
\textnormal{{Type of Structure}} & {_render_value(input_dict, KEY_STRUCTURE_TYPE)} \\[6pt]
\hline
\textnormal{{Span (m)}} & {_render_value(input_dict, KEY_SPAN, ' m')} \\[6pt]
\hline
\textnormal{{Carriageway Width (m)}} & {_render_value(input_dict, KEY_CARRIAGEWAY_WIDTH, ' m')} \\[6pt]
\hline
\textnormal{{Include Median}} & {_render_value(input_dict, KEY_INCLUDE_MEDIAN)} \\[6pt]
\hline
\textnormal{{Footpath}} & {_render_value(input_dict, KEY_FOOTPATH)} \\[6pt]
\hline
\textnormal{{Skew Angle (degrees)}} & {_render_value(input_dict, KEY_SKEW_ANGLE, '°')} (IRC 24 Cl. 504.8 limit: $\pm$15°) \\[6pt]
"""
    t_geom = lt_block("Bridge Geometry", "|L{5.5cm}|L{9.5cm}|", r"\textbf{Parameter} & \textbf{Value}",
                      t_geom_body, label="subsec:bridge-geometry", num_cols=2)

    # 3. Material Selection Table
    t_mat_body = rf"""
\textnormal{{Girder Steel Grade (IS 2062)}} & {_render_value(input_dict, KEY_GIRDER)} \\[6pt]
\hline
\textnormal{{Cross Bracing Steel Grade}} & {_render_value(input_dict, KEY_CROSS_BRACING)} \\[6pt]
\hline
\textnormal{{End Diaphragm Steel Grade}} & {_render_value(input_dict, KEY_END_DIAPHRAGM)} \\[6pt]
\hline
\textnormal{{Concrete Deck Grade (IRC 22)}} & {_render_value(input_dict, KEY_DECK_CONCRETE_GRADE_BASIC)} \\[6pt]
"""
    t_mat = lt_block("Material Selection", "|L{5.5cm}|L{9.5cm}|", r"\textbf{Parameter} & \textbf{Value}",
                     t_mat_body, label="subsec:material", num_cols=2)

    # 4. Typical Section Details
    t_typ_body = rf"""
\textnormal{{Overall Bridge Width (m)}} & {_render_value(input_dict, KEY_TS_OVERALL_WIDTH)} \\[6pt]
\hline
\textnormal{{No. of Girders}} & {_render_value(input_dict, KEY_TS_NO_OF_GIRDERS)} \\[6pt]
\hline
\textnormal{{Girder Spacing (m)}} & {_render_value(input_dict, KEY_TS_GIRDER_SPACING, ' m')} \\[6pt]
\hline
\textnormal{{Deck Overhang Width (m)}} & {_render_value(input_dict, KEY_TS_DECK_OVERHANG, ' m')} \\[6pt]
\hline
\textnormal{{Deck Thickness (mm)}} & {_render_value(input_dict, KEY_TS_DECK_THICKNESS, ' mm')} \\[6pt]
\hline
\textnormal{{Footpath Width (m)}} & {_render_value(input_dict, KEY_TS_FOOTPATH_WIDTH, ' m')} (IRC 5 Cl. 104.3.6 min: 1.5 m) \\[6pt]
\hline
\textnormal{{No. of Traffic Lanes}} & {_render_value(input_dict, KEY_WC_LD_LANE_TABLE_COUNT)} (per IRC 5 Cl. 104.3.1) \\[6pt]
"""
    t_typ = lt_block("Typical Section Details", "|L{5.5cm}|p{9.5cm}|", r"\textbf{Parameter} & \textbf{Value}",
                     t_typ_body, label="tab:typical-section", num_cols=2)

    # 5. Component Details
    t_comp_body = rf"""
\textnormal{{Crash Barrier Type}} & {_render_value(input_dict, KEY_CB_TYPE)} \\[6pt]
\hline
\textnormal{{Crash Barrier Load (kN/m)}} & {_render_value(input_dict, KEY_CB_LOAD)} \\[6pt]
\hline
{median_row}\textnormal{{Railing Type}} & {_render_value(input_dict, KEY_RL_TYPE)} \\[6pt]
\hline
\textnormal{{Railing Load (kN/m)}} & {_render_value(input_dict, KEY_RL_LOAD_VALUE)} \\[6pt]
\hline
\textnormal{{Wearing Course Material}} & {_render_value(input_dict, KEY_WC_MATERIAL)} \\[6pt]
\hline
\textnormal{{Wearing Course Thickness (mm)}} & {_render_value(input_dict, KEY_WC_THICKNESS, ' mm')} \\[6pt]
"""
    t_comp = lt_block("Components Details", "|L{5.5cm}|p{9.5cm}|", r"\textbf{Parameter} & \textbf{Value}",
                      t_comp_body, label="tab:components-details", num_cols=2)

    return rf"""
\chapter{{Input Parameters}}

This section documents all primary design inputs and bridge configuration parameters. Mandatory inputs provided directly by the user are documented alongside software-assumed defaults and code specifications (annotated with an asterisk \sdstar{{}}).

\section{{Basic Inputs (User-Defined)}}
\label{{sec:basic-inputs}}

\noindent\textit{{Note: These geometric, site, and material inputs govern the overall structural sizing.}}

{t_loc}

{t_geom}

{t_mat}

\clearpage
\section{{Additional Inputs}}
\label{{sec:additional-inputs}}

Where the user has customized additional structural parameters, those values are recorded below; standard IRC/IS software defaults are applied otherwise.

{t_typ}

{t_comp}

{_girder_tables(input_dict, n_girders)}

{_bracing_tables(input_dict, n_girders)}

{_shear_connector_table(input_dict, output_dict)}

{_safety_factors_table(input_dict)}
"""


def _girder_tables(input_dict, n_girders):
    n = n_girders if n_girders >= 1 else 1
    girder_entries = get_girder_entries(input_dict)
    if not girder_entries:
        girder_entries = [(f"Girder {i}", f"M1") for i in range(1, n + 1)]
    
    entries_for_table = [
        (lbl, mid, i)
        for i, (lbl, mid) in enumerate(
            girder_entries,
            start=1,
        )
    ]

    def _dim_row(g_lbl, i):
        return (g_lbl + r""" & """
                + (_render_value(input_dict, f"{KEY_MP_GIRDER_DEPTH}.G{i}.M1", ' mm'))
                + r""" & """
                + (_render_value(input_dict, f"{KEY_MP_GIRDER_WEB_THICKNESS}.G{i}.M1", ' mm'))
                + r""" & """
                + (_render_value(input_dict, f"{KEY_MP_GIRDER_TOP_FLANGE_WIDTH}.G{i}.M1", ' mm'))
                + ', '
                + (_render_value(input_dict, f"{KEY_MP_GIRDER_TOP_FLANGE_THICKNESS}.G{i}.M1", ' mm'))
                + r""" & """
                + (_render_value(input_dict, f"{KEY_MP_GIRDER_BOTTOM_FLANGE_WIDTH}.G{i}.M1", ' mm'))
                + ', '
                + (_render_value(input_dict, f"{KEY_MP_GIRDER_BOTTOM_FLANGE_THICKNESS}.G{i}.M1", ' mm'))
                + r""" \\[6pt]
\hline
""")

    def _gen_row(g_lbl, m_id, i):
        return (g_lbl + r""" & """ + m_id + r""" & """
                + (_render_value(input_dict, KEY_DESIGN_MODE))
                + r""" & """
                + (_render_value(input_dict, f"{KEY_MP_GIRDER_TYPE}.G{i}.M1"))
                + r""" & """
                + (_render_value(input_dict, f"{KEY_MP_GIRDER_SYMMETRY}.G{i}.M1"))
                + r""" \\[6pt]
\hline
""")

    def _rst_row(g_lbl, i):
        return (g_lbl + r""" & """
                + (_render_value(input_dict, f"{KEY_MP_GIRDER_TORSIONAL_RESTRAINT}.G{i}.M1"))
                + ', '
                + (_render_value(input_dict, f"{KEY_MP_GIRDER_WARPING_RESTRAINT}.G{i}.M1"))
                + r""" & """
                + (_render_value(input_dict, f"{KEY_MP_GIRDER_WEB_TYPE}.G{i}.M1"))
                + r""" & """
                + (_render_value(input_dict, f"{KEY_MP_STIFFENER_INTERMEDIATE}.G{i}.M1"))
                + '; Spacing: '
                + (_render_value(input_dict, f"{KEY_MP_STIFFENER_INTERMEDIATE_SPACING}.G{i}.M1", ' mm'))
                + '; Thickness: '
                + (_render_value(input_dict, f"{KEY_MP_STIFFENER_INTERMEDIATE_THICKNESS}.G{i}.M1", ' mm'))
                + r""" & """
                + (_render_value(input_dict, f"{KEY_MP_STIFFENER_LONGITUDINAL}.G{i}.M1"))
                + r""" & No.: """
                + (_render_value(input_dict, f"{KEY_MP_STIFFENER_NO_BEARING_STIFFENERS}.G{i}.M1"))
                + '; Spacing: '
                + (_render_value(input_dict, f"{KEY_MP_STIFFENER_SPACING}.G{i}.M1", ' mm'))
                + '; Thickness: '
                + (_render_value(input_dict, f"{KEY_MP_STIFFENER_BEARING_THICKNESS}.G{i}.M1", ' mm'))
                + r""" \\[6pt]
\hline
""")

    gen_rows = "".join([_gen_row(g_lbl, m_id, i) for g_lbl, m_id, i in entries_for_table])
    dim_rows = "".join([_dim_row(g_lbl, i) for g_lbl, _, i in entries_for_table])
    rst_rows = "".join([_rst_row(g_lbl, i) for g_lbl, _, i in entries_for_table])

    t_gen = lt_block("Girder General Information", "|L{2.0cm}|L{1.8cm}|p{3.8cm}|p{3.8cm}|p{3.8cm}|",
                     r"\textbf{Girder} & \textbf{Member ID} & \textbf{Design Mode} & \textbf{Girder Type} & \textbf{Girder Symmetry}",
                     gen_rows, label="tab:girder-general", num_cols=5)

    t_dim = lt_block("Girder Section Dimensions", "|L{1.8cm}|L{2.4cm}|L{1.8cm}|p{4.5cm}|p{4.5cm}|",
                     r"\textbf{Girder} & \textbf{Total Depth (mm)} & \textbf{Web $t_w$ (mm)} & \textbf{Top Flange ($b_{tf}, t_{tf}$)} & \textbf{Bottom Flange ($b_{bf}, t_{bf}$)}",
                     dim_rows, label="tab:girder-dims", num_cols=5)

    t_rst = lt_block("Girder Restraint and Stiffener Details", "|L{1.6cm}|p{2.4cm}|p{2.2cm}|p{3.2cm}|p{2.4cm}|p{3.2cm}|",
                     r"\textbf{Girder} & \textbf{Restraints} & \textbf{Web Type} & \textbf{Intermediate Stiffeners} & \textbf{Longitudinal} & \textbf{Bearing Stiffeners}",
                     rst_rows, label="tab:girder-restraints", num_cols=6)

    return f"""
\\clearpage
{t_gen}

{t_dim}

{t_rst}
"""


def _bracing_tables(input_dict, n_girders):
    n = n_girders if n_girders >= 2 else 2
    panels = [
        (
            _render_value(input_dict, f"{KEY_MP_CB_SELECT_GIRDERS}.G{i}G{i+1}.B{i}M1"),
            _render_value(input_dict, f"{KEY_MP_CB_MEMBER_ID}.G{i}G{i+1}.B{i}M1"),
            _render_value(input_dict, f"{KEY_MP_ED_SELECT_GIRDERS}.G{i}G{i+1}.E{i}M1"),
            _render_value(input_dict, f"{KEY_MP_ED_MEMBER_ID}.G{i}G{i+1}.E{i}M1"),
            i
        )
        for i in range(1, n)
    ]

    def _cb_row(location, member_ids, i):
        return (location + r""" & """ + member_ids + r""" & """
                + (_render_value(input_dict, f"{KEY_MP_CB_TYPE}.G{i}G{i+1}.B{i}M1"))
                + r""" & """
                + (_render_value(input_dict, f"{KEY_MP_CB_BRACING_SECTION_DESIGNATION}.G{i}G{i+1}.B{i}M1"))
                + r""" & """
                + (_render_value(input_dict, f"{KEY_MP_CB_SPACING}.G{i}G{i+1}.B{i}M1", ' m'))
                + r""" \\[6pt]
\hline
""")

    def _ed_row(location, member_ids, i):
        return (location + r""" & """ + member_ids + r""" & """
                + (_render_value(input_dict, f"{KEY_MP_ED_TYPE}.G{i}G{i+1}.E{i}M1"))
                + r""" & """
                + (_render_value(input_dict, f"{KEY_MP_ED_BRACING_SECTION_DESIGNATION}.G{i}G{i+1}.E{i}M1"))
                + r""" \\[6pt]
\hline
""")

    cb_rows = "".join([_cb_row(cb_loc, cb_ids, i) for cb_loc, cb_ids, _, _, i in panels])
    ed_rows = "".join([_ed_row(ed_loc, ed_ids, i) for _, _, ed_loc, ed_ids, i in panels])

    t_cb = lt_block("Member Properties: Cross Bracing Details", "|L{2.5cm}|L{2.5cm}|L{3.2cm}|L{3.5cm}|C{2.5cm}|",
                    r"\textbf{Location} & \textbf{Member IDs} & \textbf{Type of Bracing} & \textbf{Bracing Section} & \textbf{Spacing (m)}",
                    cb_rows, label="tab:cb-details", num_cols=5)

    t_ed = lt_block("Member Properties: End Diaphragm Details", "|L{3.0cm}|L{3.0cm}|L{4.2cm}|L{4.5cm}|",
                    r"\textbf{Location} & \textbf{Member IDs} & \textbf{Type of Diaphragm} & \textbf{Bracing Section}",
                    ed_rows, label="tab:ed-details", num_cols=4)

    return f"""
\\clearpage
{t_cb}

{t_ed}
"""


def _shear_connector_table(input_dict, output_dict=None):
    od = output_dict or {}
    sc_body = rf"""
\textnormal{{Stud Diameter (mm)}} & {_render_value(od, KEY_SD_SHEAR_DIAMETER, ' mm')} \\[6pt]
\hline
\textnormal{{Stud Height (mm)}} & {_render_value(od, KEY_SD_SHEAR_HEIGHT, ' mm')} \\[6pt]
\hline
\textnormal{{Stud $f_y$ (MPa)}} & {_render_value(od, KEY_SD_SHEAR_YIELD_STRENGTH, ' MPa')} \\[6pt]
\hline
\textnormal{{Stud $f_u$ (MPa)}} & {_render_value(od, KEY_SD_SHEAR_ULTIMATE_STRENGTH, ' MPa')} \\[6pt]
\hline
\textnormal{{No. of Studs per Section}} & {_render_value(od, KEY_SD_SHEAR_STUDS_PER_SECTION)} \\[6pt]
"""
    return lt_block("Shear Connector Details", "|L{5.5cm}|p{9.5cm}|", r"\textbf{Parameter} & \textbf{Value}",
                    sc_body, label="subsec:shear-connectors", num_cols=2)


def _safety_factors_table(input_dict):
    sf_body = rf"""
\textnormal{{$\gamma_{{M0}}$ (Yielding / Buckling)}} & {_render_value(input_dict, KEY_DO_GAMMA_M0)} \\[6pt]
\hline
\textnormal{{$\gamma_{{M1}}$ (Ultimate Stress)}} & {_render_value(input_dict, KEY_DO_GAMMA_M1)} \\[6pt]
\hline
\textnormal{{$\gamma_C$ (Concrete, Basic)}} & {_render_value(input_dict, KEY_DO_GAMMA_C_BASIC)} \\[6pt]
\hline
\textnormal{{$\gamma_s$ (Reinforcement)}} & {_render_value(input_dict, KEY_DO_GAMMA_S)} \\[6pt]
\hline
\textnormal{{$\gamma_v$ (Shear Connectors)}} & {_render_value(input_dict, KEY_DO_GAMMA_V)} \\[6pt]
\hline
\textnormal{{$\gamma_{{flt}}$ (Fatigue Load)}} & {_render_value(input_dict, KEY_DO_GAMMA_FLT)} \\[6pt]
\hline
\textnormal{{$\gamma_{{Mft}}$ (Fatigue Strength)}} & {_render_value(input_dict, KEY_DO_GAMMA_MF)} \\[6pt]
"""
    return lt_block("Partial Safety Factors (IRC 22 Table 1)", "|L{5.5cm}|p{9.5cm}|", r"\textbf{Parameter} & \textbf{Value}",
                    sf_body, note="All partial safety factors conform to IRC 22:2015 and IS 800:2007 requirements.",
                    label="subsec:safety-factors", num_cols=2)
