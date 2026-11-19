# =============================================================================
# Chapter 7: Material Take-off & Quantity Summary
# Includes Bill of Materials table and automated quantity visualization bar charts.
# =============================================================================

from typing import Optional
from osdagbridge.core.reports.styles import make_longtable_header, make_longtable_footer


def ch7_quantities(input_dict: dict, steel_chart_path: Optional[str] = None, conc_rebar_chart_path: Optional[str] = None) -> str:
    """
    Render Chapter 7: Material Take-off & Quantity Summary with Table 7.1 and
    programmatically embedded bar charts for steel tonnage and concrete vs rebar.
    """
    t71_header_rows = (
        r"\textbf{S.N.} & \textbf{Item Description} & \textbf{Volume} & "
        r"\textbf{Quantity} & \textbf{Total Volume} & \textbf{Weight (MT)} & \textbf{Total Weight (MT)}"
    )
    t71_col_spec = "|C{1.0cm}|L{4.2cm}|C{2.4cm}|C{1.6cm}|C{1.8cm}|C{1.8cm}|C{1.8cm}|"
    t71_hdr = make_longtable_header("Bill of Materials (Steel, Concrete, and Reinforcement Quantities)",
                                     t71_col_spec, t71_header_rows, label="tab:bill-of-materials", num_cols=7)
    lt_end = make_longtable_footer()

    # Figures block
    figures_tex = ""
    if steel_chart_path and conc_rebar_chart_path:
        sc_p = steel_chart_path.replace('\\', '/')
        cr_p = conc_rebar_chart_path.replace('\\', '/')
        figures_tex = r"""
\vspace{1.5em}
\section{Material Quantity Visualizations}
\label{sec:material-visualizations}

\noindent
The following visualizations summarize the estimated material quantities derived from the structural sizing and bill of materials:

\vspace{1.0em}
\begin{figure}[H]
\centering
\begin{minipage}[t]{0.485\textwidth}
  \centering
  \includegraphics[width=\linewidth]{""" + sc_p + r"""}
  \caption{Structural Steel Quantity Breakdown (MT)}
  \label{fig:steel-tonnage-chart}
\end{minipage}%
\hfill
\begin{minipage}[t]{0.485\textwidth}
  \centering
  \includegraphics[width=\linewidth]{""" + cr_p + r"""}
  \caption{Concrete Volume vs. Rebar Weight}
  \label{fig:concrete-rebar-chart}
\end{minipage}
\end{figure}
"""
    elif steel_chart_path:
        sc_p = steel_chart_path.replace('\\', '/')
        figures_tex = r"""
\vspace{1.5em}
\begin{figure}[H]
\centering
\includegraphics[width=0.85\textwidth]{""" + sc_p + r"""}
\caption{Structural Steel Quantity Breakdown (MT)}
\label{fig:steel-tonnage-chart}
\end{figure}
"""

    return rf"""
\chapter{{Material Take-off \& Quantity Summary}}
\label{{ch:material-takeoff}}

This chapter provides the comprehensive material take-off (Bill of Materials) for all primary superstructure components, followed by graphical summaries of structural steel tonnage and reinforced concrete consumption.

\vspace{{1.0em}}
\begingroup
\setlength{{\tabcolsep}}{{3.5pt}}
{t71_hdr}
1 & Structural Steel (IS 2062) for Girders & {str(input_dict.get("steel_girders_vol_formula", "N.A."))} & {str(input_dict.get("steel_girders_qty", "N.A."))} & {str(input_dict.get("steel_girders_vol_total", "N.A."))} & {str(input_dict.get("steel_girders_wt_single", "N.A."))} & {str(input_dict.get("steel_girders_wt_total", "N.A."))} \\
\hline
2(a) & Cross Bracing - Top Chord & {str(input_dict.get("bracing_top_vol_formula", "N.A."))} & {str(input_dict.get("bracing_top_qty", "N.A."))} & {str(input_dict.get("bracing_top_vol_total", "N.A."))} & {str(input_dict.get("bracing_top_wt_single", "N.A."))} & {str(input_dict.get("bracing_top_wt_total", "N.A."))} \\
\hline
2(b) & Cross Bracing - Bottom Chord & {str(input_dict.get("bracing_bot_vol_formula", "N.A."))} & {str(input_dict.get("bracing_bot_qty", "N.A."))} & {str(input_dict.get("bracing_bot_vol_total", "N.A."))} & {str(input_dict.get("bracing_bot_wt_single", "N.A."))} & {str(input_dict.get("bracing_bot_wt_total", "N.A."))} \\
\hline
2(c) & Cross Bracing - Diagonal Chord & {str(input_dict.get("bracing_diag_vol_formula", "N.A."))} & {str(input_dict.get("bracing_diag_qty", "N.A."))} & {str(input_dict.get("bracing_diag_vol_total", "N.A."))} & {str(input_dict.get("bracing_diag_wt_single", "N.A."))} & {str(input_dict.get("bracing_diag_wt_total", "N.A."))} \\
\hline
3 & Concrete (M40) for Deck Slab & {str(input_dict.get("concrete_deck_vol_formula", "N.A."))} & {str(input_dict.get("concrete_deck_qty", "N.A."))} & {str(input_dict.get("concrete_deck_vol_total", "N.A."))} & {str(input_dict.get("concrete_deck_wt_single", "N.A."))} & {str(input_dict.get("concrete_deck_wt_total", "N.A."))} \\
\hline
4 & Reinforcement Steel (Fe 500) & {str(input_dict.get("rebar_deck_vol_formula", "N.A."))} & {str(input_dict.get("rebar_deck_qty", "N.A."))} & {str(input_dict.get("rebar_deck_vol_total", "N.A."))} & {str(input_dict.get("rebar_deck_wt_single", "N.A."))} & {str(input_dict.get("rebar_deck_wt_total", "N.A."))} \\
\hline
5 & Shear Stud Connectors & {str(input_dict.get("shear_studs_vol_formula", "N.A."))} & {str(input_dict.get("shear_studs_qty", "N.A."))} & {str(input_dict.get("shear_studs_vol_total", "N.A."))} & {str(input_dict.get("shear_studs_wt_single", "N.A."))} & {str(input_dict.get("shear_studs_wt_total", "N.A."))} \\
\hline
6 & Crash Barrier & {str(input_dict.get("crash_barrier_vol_formula", "N.A."))} & {str(input_dict.get("crash_barrier_qty", "N.A."))} & {str(input_dict.get("crash_barrier_vol_total", "N.A."))} & {str(input_dict.get("crash_barrier_wt_single", "N.A."))} & {str(input_dict.get("crash_barrier_wt_total", "N.A."))} \\
{lt_end}
\endgroup

{figures_tex}
"""
