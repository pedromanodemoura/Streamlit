from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode, JsCode
import st_aggrid as st_ag

MAX_TABLE_HEIGHT = 500


k_sep_formatter = st_ag.JsCode("""
function(params) {
    return (params.value == null) ? params.value : params.value.toLocaleString(); 
}
""")

c_sep_formatter = st_ag.JsCode("""
function(params) {
    return (params.value == null) ? params.value : params.value.toLocaleString('en-US', {style: 'currency', currency: 'USD'}); 
}
""")

def get_numeric_style_with_precision(precision: int) -> dict:
    return {"type": ["numericColumn", "customNumericFormat"], 
            'valueFormatter': k_sep_formatter, "precision": precision}

def get_currency_style_with_precision(precision: int) -> dict:
    return {'type': ["numericColumn","customNumericFormat"], 
            'valueFormatter': c_sep_formatter, "precision": precision
            }

PRECISION_ZERO = get_numeric_style_with_precision(0)
PRECISION_ONE = get_numeric_style_with_precision(1)
PRECISION_TWO = get_numeric_style_with_precision(2)
PRECISION_TWO_DOLLAR = get_currency_style_with_precision(2)
PINLEFT = {"pinned": "left"}


def draw_grid(
        df,
        formatter: dict = None,
        selection="multiple",
        use_checkbox=False,
        fit_columns: bool = False,
        theme="streamlit",
        max_height: int = MAX_TABLE_HEIGHT,
        wrap_text: bool = False,
        auto_height: bool = False,
        grid_options: dict = None,
        key=None,
        css: dict = None
):

    gb = GridOptionsBuilder()
    gb.configure_default_column(
        filterable=True,
        groupable=False,
        editable=False,
        wrapText=wrap_text,
        autoHeight=auto_height
    )

    if grid_options is not None:
        gb.configure_grid_options(**grid_options)

    for latin_name, (cyr_name, style_dict) in formatter.items():
        gb.configure_column(latin_name, header_name=cyr_name, **style_dict)

    gb.configure_selection(selection_mode=selection, use_checkbox=use_checkbox)

    return AgGrid(
        df,
        gridOptions=gb.build(),
        update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED,
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=fit_columns,
        height=min(max_height, (2.5 + len(df.index)) * 29),
        theme=theme,
        key=key,
        custom_css=css
    )


def highlight(color, condition):
    code = f"""
        function(params) {{
            color = "{color}";
            if ({condition}) {{
                return {{
                    'backgroundColor': color
                }}
            }}
        }};
    """
    return JsCode(code)
