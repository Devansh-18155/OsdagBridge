# =============================================================================
# OsdagBridge — Centralized Formatting & Style System (Single Source of Truth)
# Defines global document settings, color palettes, custom table styles,
# page geometries, and header/footer themes.
# =============================================================================

from osdagbridge.core.reports.report_utils import _tex

# ── 1. Color Palettes ────────────────────────────────────────────────────────
COLOR_OSDAG_GREEN     = "91B014"  # Primary brand color
COLOR_OSDAG_DARK      = "556B2F"  # Secondary dark green
COLOR_PASS            = "2E7D32"  # Passing checks
COLOR_FAIL            = "C62828"  # Failing checks
COLOR_ACCENT_BLUE     = "1565C0"  # Informational highlights
COLOR_HEADER_BG       = "F2F5E8"  # Subtle table header tint
COLOR_ZEBRA_BG        = "FAFBF6"  # Alternating row background
COLOR_BORDER          = "CCCCCC"  # Subtle border lines

# ── 2. Page Geometry & Layout Dimensions ─────────────────────────────────────
PAGE_PAPER            = "a4paper"
PAGE_MARGIN_TOP       = "25mm"
PAGE_MARGIN_BOTTOM    = "28mm"
PAGE_MARGIN_LEFT      = "20mm"
PAGE_MARGIN_RIGHT     = "20mm"
HEAD_HEIGHT           = "16pt"
HEAD_SEP              = "12pt"
FOOT_SKIP             = "18mm"    # Prevents text/tables from colliding with footer

# ── 3. Table Formatting Standards ─────────────────────────────────────────────
TAB_COL_SEP           = "5pt"
ARRAY_STRETCH         = "1.15"
EXTRA_ROW_HEIGHT      = "1.5pt"
ARRAY_RULE_WIDTH      = "0.5pt"
LT_PRE                = "2pt"
LT_POST               = "6pt"

# Buffer & pagebreak rules to prevent footer overlap
NEEDSPACE_TABLE       = r"\needspace{6\baselineskip}"
NEEDSPACE_ROW         = r"\needspace{3\baselineskip}"


def make_longtable_header(caption: str, col_spec: str, header_rows: str,
                          label: str = "", num_cols: int = 2) -> str:
    r"""
    Generate standard PyLaTeX / LaTeX LongTable header with automatic repeating
    column headers on every page break (\endfirsthead and \endhead).
    """
    lbl_tex = f"\\label{{{label}}}" if label else ""
    return (
        f"\\begin{{longtable}}{{{col_spec}}}\n"
        f"\\caption{{\\textbf{{{caption}}}}}{lbl_tex}\\\\\n"
        f"\\hline\n"
        f"{header_rows} \\\\[6pt]\n"
        f"\\hline\n"
        f"\\endfirsthead\n\n"
        f"\\multicolumn{{{num_cols}}}{{c}}{{\\small\\textit{{\\tablename\\ \\thetable{{}} -- Continued from previous page}}}} \\\\[4pt]\n"
        f"\\hline\n"
        f"{header_rows} \\\\[6pt]\n"
        f"\\hline\n"
        f"\\endhead\n\n"
        f"\\hline\n"
        f"\\multicolumn{{{num_cols}}}{{|r|}}{{\\footnotesize\\textit{{Continued on next page\\dots}}}} \\\\\n"
        f"\\hline\n"
        f"\\endfoot\n\n"
        f"\\hline\n"
        f"\\endlastfoot\n"
    )


def make_longtable_footer() -> str:
    """Standard LongTable termination."""
    return "\\end{longtable}\n"


def lt_block(caption: str, col_spec: str, header_rows: str, body_rows: str,
             note: str = "", label: str = "", num_cols: int = 2) -> str:
    """
    Complete self-contained LongTable block with caption, repeating headers,
    body rows, and optional footnote.
    """
    hdr = make_longtable_header(caption, col_spec, header_rows, label=label, num_cols=num_cols)
    ftr = make_longtable_footer()
    note_tex = f"\n\\noindent\\textit{{Note: {note}}}\n" if note else ""
    return f"\n\\vspace{{0.8em}}\n{hdr}\n{body_rows}\n{ftr}{note_tex}\n"


def generate_preamble(project_name: str, job_number: str, report_date: str, report_version: str = 'Rev 0') -> str:
    """
    Generate the master LaTeX preamble consuming all centralized design tokens.
    """
    pn = _tex(project_name)
    jn = _tex(job_number)
    rd = _tex(report_date)
    rv = _tex(report_version)

    return f"""
\\documentclass[12pt,{PAGE_PAPER}]{{report}}

% ── Geometry & Layout ────────────────────────────────────────────────────────
\\usepackage[{PAGE_PAPER}, top={PAGE_MARGIN_TOP}, bottom={PAGE_MARGIN_BOTTOM}, left={PAGE_MARGIN_LEFT}, right={PAGE_MARGIN_RIGHT}, headheight={HEAD_HEIGHT}, headsep={HEAD_SEP}, footskip={FOOT_SKIP}]{{geometry}}
\\usepackage{{graphicx}}
\\usepackage{{amsmath}}
\\usepackage{{amssymb}}
\\usepackage{{booktabs}}
\\usepackage{{array}}
\\usepackage{{tabularx}}
\\usepackage{{float}}
\\usepackage{{fancyhdr}}
\\usepackage[hidelinks]{{hyperref}}
\\usepackage{{xcolor}}
\\usepackage{{setspace}}
\\usepackage{{enumitem}}
\\usepackage{{caption}}

\\captionsetup{{
    labelfont=bf,
    justification=raggedright,
    singlelinecheck=false,
    format=plain
}}
\\usepackage{{subcaption}}
\\usepackage{{multirow}}
\\usepackage{{colortbl}}
\\usepackage{{longtable}}
\\setlength{{\\LTleft}}{{\\fill}}
\\setlength{{\\LTright}}{{\\fill}}
\\usepackage{{titlesec}}
\\usepackage{{titletoc}}
\\usepackage{{lastpage}}
\\usepackage{{makecell}}
\\usepackage{{etoolbox}}
\\usepackage{{needspace}}

\\numberwithin{{table}}{{chapter}}
\\numberwithin{{figure}}{{chapter}}

% ── Table Layout Standards (Centralized) ────────────────────────────────────
\\setlength{{\\tabcolsep}}{{{TAB_COL_SEP}}}
\\renewcommand{{\\arraystretch}}{{{ARRAY_STRETCH}}}
\\setlength{{\\extrarowheight}}{{{EXTRA_ROW_HEIGHT}}}
\\setlength{{\\arrayrulewidth}}{{{ARRAY_RULE_WIDTH}}}
\\setlength{{\\LTpre}}{{{LT_PRE}}}
\\setlength{{\\LTpost}}{{{LT_POST}}}

% Threshold constraints: break page before large blocks if insufficient space
\\BeforeBeginEnvironment{{table}}{{\\needspace{{5\\baselineskip}}}}
\\BeforeBeginEnvironment{{longtable}}{{\\needspace{{6\\baselineskip}}}}

% ── Centralized Colors ──────────────────────────────────────────────────────
\\definecolor{{osdagGreen}}{{HTML}}{{{COLOR_OSDAG_GREEN}}}
\\definecolor{{osdagDark}}{{HTML}}{{{COLOR_OSDAG_DARK}}}
\\definecolor{{passGreen}}{{HTML}}{{{COLOR_PASS}}}
\\definecolor{{failRed}}{{HTML}}{{{COLOR_FAIL}}}
\\definecolor{{headerBg}}{{HTML}}{{{COLOR_HEADER_BG}}}
\\definecolor{{zebraBg}}{{HTML}}{{{COLOR_ZEBRA_BG}}}
\\definecolor{{ruleBorder}}{{HTML}}{{{COLOR_BORDER}}}

% ── Header and Footer Styles ────────────────────────────────────────────────
\\fancypagestyle{{main}}{{
  \\fancyhf{{}}
  \\fancyhead[L]{{{pn} $|$ {jn}}}
  \\fancyhead[R]{{{rd} $|$ {rv}}}
  \\fancyfoot[L]{{Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay}}
  \\fancyfoot[R]{{Page \\thepage\\ of \\pageref{{LastPage}}}}
  \\renewcommand{{\\headrule}}{{\\color{{osdagGreen}}\\hrule width\\headwidth height 1pt \\vspace{{2pt}}}}
  \\renewcommand{{\\footrule}}{{%
    \\ifbool{{hasSDonPage}}{{%
      \\vspace{{-4pt}}%
      \\hbox to \\headwidth{{\\textcolor{{black}}{{\\footnotesize\\textit{{* Software default value}}}}\\hfil}}%
      \\vspace{{2pt}}%
    }}{{%
      \\vspace{{0pt}}%
    }}%
    \\color{{osdagGreen}}\\hrule width\\headwidth height 1pt \\vspace{{4pt}}%
  }}
}}
\\fancypagestyle{{plain}}{{
  \\fancyhf{{}}
  \\fancyhead[L]{{{pn} $|$ {jn}}}
  \\fancyhead[R]{{{rd} $|$ {rv}}}
  \\fancyfoot[L]{{Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay}}
  \\fancyfoot[R]{{Page \\thepage\\ of \\pageref{{LastPage}}}}
  \\renewcommand{{\\headrule}}{{\\color{{osdagGreen}}\\hrule width\\headwidth height 1pt \\vspace{{2pt}}}}
  \\renewcommand{{\\footrule}}{{%
    \\ifbool{{hasSDonPage}}{{%
      \\vspace{{-4pt}}%
      \\hbox to \\headwidth{{\\textcolor{{black}}{{\\footnotesize\\textit{{* Software default value}}}}\\hfil}}%
      \\vspace{{2pt}}%
    }}{{%
      \\vspace{{0pt}}%
    }}%
    \\color{{osdagGreen}}\\hrule width\\headwidth height 1pt \\vspace{{4pt}}%
  }}
}}
\\fancypagestyle{{firstpage}}{{
  \\fancyhf{{}}
  \\renewcommand{{\\headrulewidth}}{{0pt}}
  \\fancyfoot[L]{{Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay}}
  \\fancyfoot[R]{{Page \\thepage\\ of \\pageref{{LastPage}}}}
  \\renewcommand{{\\footrule}}{{\\color{{osdagGreen}}\\hrule width\\headwidth height 1pt \\vspace{{4pt}}}}
}}
\\pagestyle{{main}}
\\setstretch{{1.15}}

% ── Column Types ────────────────────────────────────────────────────────────
\\newcommand{{\\placeholder}}[1]{{\\textit{{\\textless #1\\textgreater}}}}
\\newcolumntype{{L}}[1]{{>{{\\raggedright\\arraybackslash}}p{{#1}}}}
\\newcolumntype{{C}}[1]{{>{{\\centering\\arraybackslash}}p{{#1}}}}
\\newcolumntype{{R}}[1]{{>{{\\raggedleft\\arraybackslash}}p{{#1}}}}

% ── Software-Default Asterisk Tracker ───────────────────────────────────────
\\newcommand{{\\sdstar}}{{\\textsuperscript{{*}}}}
\\newbool{{hasSDonPage}}
\\boolfalse{{hasSDonPage}}
\\newcommand{{\\markSD}}{{\\global\\booltrue{{hasSDonPage}}}}
\\renewcommand{{\\sdstar}}{{\\textsuperscript{{*}}\\markSD{{}}}}
\\AddToHook{{shipout/before}}{{\\global\\boolfalse{{hasSDonPage}}}}

% ── Section Heading Styling ─────────────────────────────────────────────────
\\titleformat{{\\section}}
  {{\\normalfont\\large\\bfseries\\color{{black}}}}
  {{\\thesection}}{{1em}}{{}}

\\titleformat{{\\subsection}}
  {{\\normalfont\\normalsize\\bfseries\\color{{black}}}}
  {{\\thesubsection}}{{1em}}{{}}

\\titleformat{{\\chapter}}[hang]
  {{\\normalfont\\Large\\bfseries\\color{{black}}}}
  {{\\thechapter}}{{1em}}{{}}
\\titlespacing*{{\\chapter}}{{0pt}}{{0pt}}{{12pt}}
"""
