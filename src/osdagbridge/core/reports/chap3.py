# =============================================================================
# Chapter 3: Loads and Load Combinations
# Refactored for clean separation of Live Loads and Footpath Loads,
# structured parameter columns, and repeated LongTable headers.
# =============================================================================

from osdagbridge.core.utils.common import (
    KEY_CB_LOAD,
    KEY_LL_CUSTOM_VEHICLES,
    KEY_LL_FOOTPATH_PRESSURE_MODE,
    KEY_LL_FOOTPATH_PRESSURE_VALUE,
    KEY_LL_IRC_70R_BOGIE,
    KEY_LL_IRC_70R_TRACKED,
    KEY_LL_IRC_70R_WHEELED,
    KEY_LL_IRC_AA_TRACKED,
    KEY_LL_IRC_AA_WHEELED,
    KEY_LL_IRC_CLASS_A,
    KEY_LL_IRC_CLASS_FATIGUE,
    KEY_LL_IRC_CLASS_SV,
    KEY_MATERIAL_DECK_DENSITY,
    KEY_MATERIAL_GIRDER_DENSITY,
    KEY_PL_SELF_WEIGHT_FACTOR,
    KEY_RL_LOAD_VALUE,
    KEY_SL_DAMPING,
    KEY_SL_DEAD_LOAD_MODE,
    KEY_SL_DEAD_LOAD_VALUE,
    KEY_SL_HORIZONTAL_COEFF,
    KEY_SL_IMPORTANCE_FACTOR,
    KEY_SL_LIVE_LOAD_MODE,
    KEY_SL_LIVE_LOAD_VALUE,
    KEY_SL_SEISMIC_ZONE,
    KEY_SL_SOIL_TYPE,
    KEY_SL_SPECTRAL_COEFF,
    KEY_SL_TIME_PERIOD,
    KEY_SL_VERTICAL_COEFF,
    KEY_SL_ZONE_FACTOR,
    KEY_SPAN,
    KEY_TL_BRIDGE_TEMP_MAX,
    KEY_TL_BRIDGE_TEMP_MIN,
    KEY_TL_HIGHEST_MAX_TEMP,
    KEY_TL_LOWEST_MIN_TEMP,
    KEY_TL_TEMP_FALL,
    KEY_TL_TEMP_RISE,
    KEY_TS_FOOTPATH_WIDTH,
    KEY_WC_LD_LANE_TABLE_COUNT,
    KEY_WC_MATERIAL,
    KEY_WC_THICKNESS,
    KEY_WL_AVG_EXPOSED_HEIGHT,
    KEY_WL_BASIC_WIND_SPEED,
    KEY_WL_HOURLY_MEAN_WIND,
    KEY_WL_HOURLY_WIND_PRESSURE,
    KEY_WL_LONGITUDINAL_WIND_FORCE,
    KEY_WL_TERRAIN_TYPE,
    KEY_WL_TRANSVERSE_WIND_FORCE,
    KEY_WL_VERTICAL_WIND_FORCE
)

from osdagbridge.core.reports.report_utils import _tex, _render_value
from osdagbridge.core.reports.styles import make_longtable_header, make_longtable_footer


def ch3_loads(input_dict):
    from osdagbridge.core.utils.codes.irc6_2017 import IRC6_2017
    span = input_dict.get(KEY_SPAN)
    span_m = float(span) if span not in (None, "") else 0.0

    # ── 1. Determine Vehicles Selected in UI ─────────────────────────────────
    # Standard vehicular live load database per IRC 6:2017
    # (Total load in kN, standard impact factor formula, braking applicability)
    vehicle_specs = []

    # Calculate span-dependent impact factors
    im_a = IRC6_2017.cl_208_2_impact_factor(span_m) if span_m > 0 else 0.0
    im_heavy = IRC6_2017.cl_208_3_impact_factor(span_m) if span_m > 0 else 0.0

    lanes_val = input_dict.get(KEY_WC_LD_LANE_TABLE_COUNT, 2)
    try:
        lanes_int = int(lanes_val)
    except Exception:
        lanes_int = 2
    # IRC 6:2017 Clause 211.2: 20% of Class A vehicle load (554 kN) for first 2 lanes,
    # plus 5% of Class 70R (1000 kN) for each additional lane
    braking_force_kN = 0.20 * 554.0
    if lanes_int > 2:
        braking_force_kN += 0.05 * 1000.0 * (lanes_int - 2)

    # Check vehicle flags
    has_class_a = bool(input_dict.get(KEY_LL_IRC_CLASS_A))
    has_70r_w   = bool(input_dict.get(KEY_LL_IRC_70R_WHEELED))
    has_70r_t   = bool(input_dict.get(KEY_LL_IRC_70R_TRACKED))
    has_aa_w    = bool(input_dict.get(KEY_LL_IRC_AA_WHEELED))
    has_aa_t    = bool(input_dict.get(KEY_LL_IRC_AA_TRACKED))
    has_sv      = bool(input_dict.get(KEY_LL_IRC_CLASS_SV))
    has_70r_b   = bool(input_dict.get(KEY_LL_IRC_70R_BOGIE))
    has_fatigue = bool(input_dict.get(KEY_LL_IRC_CLASS_FATIGUE))

    # If nothing explicitly flagged, default to standard IRC Class A + 70R
    if not any([has_class_a, has_70r_w, has_70r_t, has_aa_w, has_aa_t, has_sv, has_70r_b, has_fatigue]):
        has_class_a = True
        has_70r_w = True

    if has_class_a:
        vehicle_specs.append({
            "name": "Class A",
            "total_load": "554.0",
            "impact": f"{1.0 + im_a:.3f}",
            "braking_considered": "Yes",
            "braking_val": f"{braking_force_kN:.1f} kN",
            "braking_ecc": "1.2 m",
        })
    if has_70r_w:
        vehicle_specs.append({
            "name": "Class 70R (Wheeled)",
            "total_load": "1000.0",
            "impact": f"{1.0 + im_heavy:.3f}",
            "braking_considered": "Yes",
            "braking_val": f"{braking_force_kN:.1f} kN",
            "braking_ecc": "1.2 m",
        })
    if has_70r_t:
        vehicle_specs.append({
            "name": "Class 70R (Tracked)",
            "total_load": "700.0",
            "impact": f"{1.0 + min(0.10, im_heavy):.3f}",
            "braking_considered": "Yes",
            "braking_val": f"{braking_force_kN:.1f} kN",
            "braking_ecc": "1.2 m",
        })
    if has_aa_w:
        vehicle_specs.append({
            "name": "Class AA (Wheeled)",
            "total_load": "400.0",
            "impact": f"{1.0 + im_heavy:.3f}",
            "braking_considered": "Yes",
            "braking_val": f"{braking_force_kN:.1f} kN",
            "braking_ecc": "1.2 m",
        })
    if has_aa_t:
        vehicle_specs.append({
            "name": "Class AA (Tracked)",
            "total_load": "700.0",
            "impact": f"{1.0 + min(0.10, im_heavy):.3f}",
            "braking_considered": "Yes",
            "braking_val": f"{braking_force_kN:.1f} kN",
            "braking_ecc": "1.2 m",
        })
    if has_sv:
        vehicle_specs.append({
            "name": "Class SV",
            "total_load": "3850.0",
            "impact": "1.000",
            "braking_considered": "No",
            "braking_val": "---",
            "braking_ecc": "---",
        })
    if has_70r_b:
        vehicle_specs.append({
            "name": "Class 70R (Bogie)",
            "total_load": "400.0",
            "impact": f"{1.0 + im_heavy:.3f}",
            "braking_considered": "Yes",
            "braking_val": f"{braking_force_kN:.1f} kN",
            "braking_ecc": "1.2 m",
        })
    if has_fatigue:
        vehicle_specs.append({
            "name": "Class Fatigue",
            "total_load": "400.0",
            "impact": "1.000",
            "braking_considered": "No",
            "braking_val": "---",
            "braking_ecc": "---",
        })

    # Custom vehicles
    custom = input_dict.get(KEY_LL_CUSTOM_VEHICLES)
    if custom and isinstance(custom, list):
        for c in custom:
            c_name = c.get('name', 'Custom Vehicle') if isinstance(c, dict) else str(c)
            c_load = f"{float(c.get('total_load', 500.0)):.1f}" if isinstance(c, dict) and c.get('total_load') else "---"
            vehicle_specs.append({
                "name": c_name,
                "total_load": c_load,
                "impact": f"{1.0 + im_a:.3f}",
                "braking_considered": "Yes",
                "braking_val": f"{braking_force_kN:.1f} kN",
                "braking_ecc": "1.2 m",
            })

    # Build Vehicle Live Loads Rows
    vehicle_rows = []
    for vs in vehicle_specs:
        vehicle_rows.append(
            f"\\textnormal{{{_tex(vs['name'])}}} & {vs['total_load']} & {vs['impact']} & "
            f"{vs['braking_considered']} & {vs['braking_val']} & {vs['braking_ecc']} \\\\[6pt]\n\\hline"
        )
    vehicle_rows_str = "\n".join(vehicle_rows)

    # ── 2. Footpath Live Load Processing ─────────────────────────────────────
    fp_mode  = input_dict.get(KEY_LL_FOOTPATH_PRESSURE_MODE, "Automatic")
    fp_value = input_dict.get(KEY_LL_FOOTPATH_PRESSURE_VALUE, "")
    fp_width = input_dict.get(KEY_TS_FOOTPATH_WIDTH, "1.5")
    
    try:
        fp_w_float = float(fp_width) if fp_width not in (None, "") else 0.0
    except Exception:
        fp_w_float = 0.0

    if str(fp_mode).strip().lower() in ("as per irc 6", "as per irc6", "automatic", "standard"):
        try:
            fp_intensity_val = IRC6_2017.cl_206_1_footway_load()
            fp_intensity_str = f"{fp_intensity_val:.3f} kN/m²"
            fp_ref = "IRC 6:2017 Cl. 206.1"
        except Exception:
            fp_intensity_val = 4.0
            fp_intensity_str = "4.000 kN/m²"
            fp_ref = "IRC 6:2017 Cl. 206.1"
    elif fp_value not in (None, ""):
        try:
            fp_intensity_val = float(fp_value)
            fp_intensity_str = f"{fp_intensity_val:.3f} kN/m²"
            fp_ref = "User Defined Custom Value"
        except Exception:
            fp_intensity_val = 0.0
            fp_intensity_str = f"{fp_value} kN/m²"
            fp_ref = "User Defined"
    else:
        fp_intensity_val = 0.0
        fp_intensity_str = "Not Applicable"
        fp_ref = "---"

    fp_total_linear = f"{fp_intensity_val * fp_w_float:.2f} kN/m" if fp_w_float > 0 else "0.00 kN/m"

    # ── 3. Environmental Loads (Wind, Seismic, Temp) ─────────────────────────
    vz_val = input_dict.get(KEY_WL_HOURLY_MEAN_WIND)
    pz_val = input_dict.get(KEY_WL_HOURLY_WIND_PRESSURE)
    if not vz_val or not pz_val:
        try:
            _vb  = input_dict.get(KEY_WL_BASIC_WIND_SPEED) or input_dict.get('wind_speed')
            _h   = input_dict.get(KEY_WL_AVG_EXPOSED_HEIGHT)
            _ter = {
                "Plain Terrain": "plain",
                "Terrain with Obstructions": "obstructed",
            }.get(str(input_dict.get(KEY_WL_TERRAIN_TYPE, "")).strip(), "plain")
            _res = IRC6_2017.table_12(float(_h), _ter, float(_vb))
            if not vz_val:
                vz_val = _res.get("Vz")
            if not pz_val:
                pz_val = _res.get("Pz")
        except Exception:
            pass

    sl_zone_factor = input_dict.get(KEY_SL_ZONE_FACTOR)
    sl_spectral    = input_dict.get(KEY_SL_SPECTRAL_COEFF)
    sl_ah          = input_dict.get(KEY_SL_HORIZONTAL_COEFF)
    sl_av          = input_dict.get(KEY_SL_VERTICAL_COEFF)
    if not sl_ah or not sl_zone_factor:
        try:
            _zone = input_dict.get(KEY_SL_SEISMIC_ZONE) or input_dict.get('seismic_zone')
            _zmap = {"1": "I", "2": "II", "3": "III", "4": "IV", "5": "V"}
            _z    = str(_zone).strip().upper()
            if _z.isdigit():
                _z = _zmap.get(_z)
            _smap = {"Type I – Rocky or Hard": 1, "Type II – Medium Soil": 2, "Type III – Soft Soil": 3}
            _st   = _smap.get(str(input_dict.get(KEY_SL_SOIL_TYPE, "")), 1)
            _tp   = input_dict.get(KEY_SL_TIME_PERIOD)
            _damp = input_dict.get(KEY_SL_DAMPING) or "5"
            _dl_v = input_dict.get(KEY_SL_DEAD_LOAD_VALUE)
            _ll_v = input_dict.get(KEY_SL_LIVE_LOAD_VALUE)
            _dead = float(_dl_v) if str(input_dict.get(KEY_SL_DEAD_LOAD_MODE, "")) == "Custom" and _dl_v else 0.0
            _live = float(_ll_v) if str(input_dict.get(KEY_SL_LIVE_LOAD_MODE, "")) == "Custom" and _ll_v else 0.0
            _res  = IRC6_2017.cl_218_5_1(zone=f"Zone {_z}", soil_type=_st, dead_load_kN=_dead,
                        live_load_kN=_live, period_T=float(_tp) if _tp else None,
                        damping_percent=float(_damp))
            if not sl_zone_factor:
                sl_zone_factor = _res.get("Z")
            if not sl_spectral:
                sl_spectral    = _res.get("Sa_g_adjusted")
            if not sl_ah:
                sl_ah          = _res.get("Ah")
            if not sl_av:
                sl_av          = round(_res.get("Ah", 0) * 2 / 3, 4)
        except Exception:
            pass

    # Temperature Load
    tl_temp_min = input_dict.get(KEY_TL_BRIDGE_TEMP_MIN, "N/A")
    tl_temp_max = input_dict.get(KEY_TL_BRIDGE_TEMP_MAX, "N/A")
    tl_rise     = input_dict.get(KEY_TL_TEMP_RISE, "N/A")
    tl_fall     = input_dict.get(KEY_TL_TEMP_FALL, "N/A")

    # ── 4. Load Combinations ─────────────────────────────────────────────────
    _LOAD_LABEL_MAP = {
        'dead_load':         'DL',
        'surfacing':         'SIDL',
        'live_load':         'LL',
        'wind_load':         'WL',
        'thermal_load':      'TL',
        'vehicle_collision': 'VC',
        'barge_impact':      'BI',
        'floating_bodies':   'FB',
        'seismic':           'EQ',
    }

    def _fmt_factors(factors):
        parts = []
        for load, val in factors.items():
            label = _LOAD_LABEL_MAP.get(load, load.upper())
            if isinstance(val, dict):
                add = val.get('adding')
                rel = val.get('relieving')
                add_s = f"{add:.2f}" if add is not None else '--'
                rel_s = f"{rel:.2f}" if rel is not None else '--'
                parts.append(f"{label}({add_s}/{rel_s})")
            else:
                if val is None:
                    continue
                parts.append(f"{label}({val:.2f})")
        return ' + '.join(parts)

    uls_combos = IRC6_2017.uls_load_combinations()
    sls_combos = IRC6_2017.sls_load_combinations()
    lc_rows = []
    for i, combo in enumerate(uls_combos, start=1):
        cases = _fmt_factors(combo['factors'])
        lc_rows.append(f"ULS-{i:02d} & {cases} \\\\[6pt]\n\\hline")
    for i, combo in enumerate(sls_combos, start=1):
        cases = _fmt_factors(combo['factors'])
        lc_rows.append(f"SLS-{i:02d} & {cases} \\\\[6pt]\n\\hline")
    lc_rows_str = "\n".join(lc_rows)

    # ── Construct LongTables with Repeated Headers ───────────────────────────
    # Table 3.1: Dead Load - Self Weight
    t31_hdr = make_longtable_header("Dead Load -- Self Weight", "|L{5.5cm}|p{9.5cm}|",
                                     r"\textbf{Parameter} & \textbf{Value}", label="tab:dead-load-sw", num_cols=2)
    # Table 3.2: Dead Load for Surfacing
    t32_hdr = make_longtable_header("Dead Load for Surfacing (DW)", "|L{5.5cm}|p{9.5cm}|",
                                     r"\textbf{Parameter} & \textbf{Value}", label="tab:dead-load-dw", num_cols=2)
    
    # Table 3.3: Vehicle Live Loads (Refactored per specification)
    t33_header_rows = (
        r"\multirow{2}{*}{\textbf{Vehicle Class}} & \multirow{2}{*}{\textbf{Total Load (kN)}} & \multirow{2}{*}{\textbf{Impact Factor}} & \multicolumn{3}{c|}{\textbf{Braking Load}} \\" + "\n"
        r"\cline{4-6}" + "\n"
        r"& & & \textbf{Considered?} & \textbf{Value} & \textbf{Eccentricity}"
    )
    t33_col_spec = "|L{3.2cm}|C{2.2cm}|C{2.0cm}|C{2.0cm}|C{2.6cm}|C{2.2cm}|"
    t33_hdr = make_longtable_header("Vehicular Live Loads (LL) --- per IRC 6", t33_col_spec,
                                     t33_header_rows, label="tab:vehicular-live-loads", num_cols=6)

    # Table 3.4: Footpath Live Load (Separated table per specification)
    t34_hdr = make_longtable_header("Footpath Live Load --- per IRC 6", "|L{5.5cm}|p{5.5cm}|p{4.0cm}|",
                                     r"\textbf{Parameter} & \textbf{Design Value} & \textbf{Code Reference}", label="tab:footpath-loads", num_cols=3)

    # Table 3.5: Wind Load
    t35_hdr = make_longtable_header("Wind Load (WL) --- per IRC 6", "|L{5.5cm}|p{9.5cm}|",
                                     r"\textbf{Parameter} & \textbf{Value}", label="tab:wind-load", num_cols=2)

    # Table 3.6: Earthquake Load
    t36_hdr = make_longtable_header("Earthquake Load (EL) --- per IRC 6", "|L{5.5cm}|p{9.5cm}|",
                                     r"\textbf{Parameter} & \textbf{Value}", label="tab:earthquake-load", num_cols=2)

    # Table 3.7: Temperature Load
    t37_hdr = make_longtable_header("Temperature Load (TL) --- per IRC 6", "|L{5.5cm}|p{9.5cm}|",
                                     r"\textbf{Parameter} & \textbf{Value}", label="tab:temp-load", num_cols=2)

    # Table 3.8: Load Combinations
    t38_hdr = make_longtable_header("Load Combinations (ULS & SLS) --- per IRC 6", "|C{3.2cm}|p{12.0cm}|",
                                     r"\textbf{Combination ID} & \textbf{Factored Load Cases}", label="tab:load-combos", num_cols=2)

    lt_end = make_longtable_footer()

    return rf"""
\chapter{{Loads and Load Combinations}}

This section summarizes all permanent, transient, and environmental loads applied to the bridge, followed by the complete matrix of limit-state load combinations generated per IRC~6:2017.

\vspace{{0.8em}}
{t31_hdr}
\textnormal{{Steel Self-Weight Applied}} & {(_render_value(input_dict, KEY_MATERIAL_GIRDER_DENSITY, ' kN/m\\textsuperscript{3}'))} \\[6pt]
\hline
\textnormal{{Concrete Deck Weight}} & {(_render_value(input_dict, KEY_MATERIAL_DECK_DENSITY, ' kN/m\\textsuperscript{3}'))} \\[6pt]
\hline
\textnormal{{Self-Weight Factor}} & {(_render_value(input_dict, KEY_PL_SELF_WEIGHT_FACTOR))} \\[6pt]
{lt_end}

\vspace{{0.8em}}
{t32_hdr}
\textnormal{{Wearing Course Load}} & {(_render_value(input_dict, KEY_WC_MATERIAL))} $\times$ {(_render_value(input_dict, KEY_WC_THICKNESS))} \\[6pt]
\hline
\textnormal{{Additional SIDL (Crash Barrier)}} & {(_render_value(input_dict, KEY_CB_LOAD))} kN/m per barrier \\[6pt]
\hline
\textnormal{{Railing Load}} & {(_render_value(input_dict, KEY_RL_LOAD_VALUE))} kN/m\sdstar{{}} \\[6pt]
{lt_end}

\vspace{{0.8em}}
{t33_hdr}
{vehicle_rows_str}
{lt_end}
\noindent\textit{{Note: Live load parameters reflect vehicular classes selected in additional inputs. Impact factors and braking loads are determined strictly in compliance with IRC 6:2017 Cl. 208 and Cl. 211.2.}}

\vspace{{1.2em}}
{t34_hdr}
\textnormal{{Footpath Loading Mode}} & {_tex(str(fp_mode))} & Clause 206.1 \\[6pt]
\hline
\textnormal{{Footpath Width}} & {_tex(str(fp_width))} m & Typical Section Input \\[6pt]
\hline
\textnormal{{Footpath Live Load Intensity}} & {fp_intensity_str} & {fp_ref} \\[6pt]
\hline
\textnormal{{Total Linear Footpath Load}} & {fp_total_linear} & Intensity $\times$ Width \\[6pt]
\hline
\textnormal{{Application Status}} & Pedestrian traffic on sidewalk & Active in Live Load Combos \\[6pt]
{lt_end}

\vspace{{0.8em}}
{t35_hdr}
\textnormal{{Basic Wind Speed, Vb}} & {(_render_value(input_dict, 'wind_speed', ' m/s'))} [from Project Location] \\[6pt]
\hline
\textnormal{{Terrain Type}} & {(_render_value(input_dict, KEY_WL_TERRAIN_TYPE))} \\[6pt]
\hline
\textnormal{{Average Exposed Height, H (m)}} & {(_render_value(input_dict, KEY_WL_AVG_EXPOSED_HEIGHT, ' m'))} \\[6pt]
\hline
\textnormal{{Hourly Mean Wind Speed, Vz}} & {(_render_value(input_dict, KEY_WL_HOURLY_MEAN_WIND, ' m/s'))} \\[6pt]
\hline
\textnormal{{Hourly Wind Pressure, Pz}} & {(_render_value(input_dict, KEY_WL_HOURLY_WIND_PRESSURE, ' N/m\\textsuperscript{2}'))} \\[6pt]
\hline
\textnormal{{Transverse Wind Force}} & {(_render_value(input_dict, KEY_WL_TRANSVERSE_WIND_FORCE, ' kN'))} \\[6pt]
\hline
\textnormal{{Longitudinal Wind Force}} & {(_render_value(input_dict, KEY_WL_LONGITUDINAL_WIND_FORCE, ' kN'))} \\[6pt]
\hline
\textnormal{{Vertical Wind Force}} & {(_render_value(input_dict, KEY_WL_VERTICAL_WIND_FORCE, ' kN'))} \\[6pt]
{lt_end}

\vspace{{0.8em}}
{t36_hdr}
\textnormal{{Seismic Zone}} & {(_render_value(input_dict, 'seismic_zone'))} [from Project Location] \\[6pt]
\hline
\textnormal{{Zone Factor, Z}} & {(_render_value(input_dict, KEY_SL_ZONE_FACTOR))} \\[6pt]
\hline
\textnormal{{Importance Factor, I}} & {(_render_value(input_dict, KEY_SL_IMPORTANCE_FACTOR))} \\[6pt]
\hline
\textnormal{{Type of Soil}} & {(_render_value(input_dict, KEY_SL_SOIL_TYPE))} \\[6pt]
\hline
\textnormal{{Sa/g}} & {(_render_value(input_dict, KEY_SL_SPECTRAL_COEFF))} \\[6pt]
\hline
\textnormal{{Horizontal Seismic Coefficient, Ah}} & {(_render_value(input_dict, KEY_SL_HORIZONTAL_COEFF))} \\[6pt]
\hline
\textnormal{{Vertical Seismic Coefficient, Av}} & {(_render_value(input_dict, KEY_SL_VERTICAL_COEFF))} \\[6pt]
{lt_end}

\vspace{{0.8em}}
{t37_hdr}
\textnormal{{Maximum Shade Temperature}} & {(_render_value(input_dict, 'shade_temp_max'))} $^\circ$C \\[6pt]
\hline
\textnormal{{Minimum Shade Temperature}} & {(_render_value(input_dict, 'shade_temp_min'))} $^\circ$C \\[6pt]
\hline
\textnormal{{Effective Bridge Temp. Range}} & {_tex(str(tl_temp_min))} to {_tex(str(tl_temp_max))} $^\circ$C \\[6pt]
\hline
\textnormal{{Temperature Rise / Fall for Design}} & +{_tex(str(tl_rise))} $^\circ$C / \textminus{{}}{_tex(str(tl_fall))} $^\circ$C \\[6pt]
{lt_end}

\vspace{{0.8em}}
{t38_hdr}
{lc_rows_str}
{lt_end}
\noindent\textit{{Note: All IRC 6:2017 ultimate and serviceability load combinations are dynamically evaluated for maximum structural actions.}}
"""
