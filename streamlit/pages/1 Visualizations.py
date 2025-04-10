import streamlit as st
import streamlit.components.v1 as components

st.title("Let's see some graphs in Tableau!")
st.write("To see the graphs bigger, click on the 'Full screen' button on the bottom right.")

st.markdown("#### There are many tabs, don't just stay on the first one.")
col1, col2 = st.columns([0.15, 0.85])
with col2:
    st.write(":point_down:")

def main():
    html_temp = """
    <div class='tableauPlaceholder' id='viz1744217560400' style='position: relative'>
        <noscript>
            <a href='#'>
                <img alt=' ' src='https://public.tableau.com/static/images/Wh/Whattherock/Subgenresstyles/1_rss.png' style='border: none' />
            </a>
        </noscript>
        <object class='tableauViz'>
            <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
            <param name='embed_code_version' value='3' />
            <param name='site_root' value='' />
            <param name='name' value='Whattherock/Subgenresstyles' />
            <param name='tabs' value='yes' />
            <param name='toolbar' value='yes' />
            <param name='static_image' value='https://public.tableau.com/static/images/Wh/Whattherock/Subgenresstyles/1.png' />
            <param name='animate_transition' value='yes' />
            <param name='display_static_image' value='yes' />
            <param name='display_spinner' value='yes' />
            <param name='display_overlay' value='yes' />
            <param name='display_count' value='yes' />
            <param name='language' value='es-ES' />
        </object>
    </div>
    <script type='text/javascript'>
        var divElement = document.getElementById('viz1744217560400');
        var vizElement = divElement.getElementsByTagName('object')[0];

        vizElement.style.width = '100%';  // 100% of the container width
        vizElement.style.height = '860px';

        var scriptElement = document.createElement('script');
        scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
        vizElement.parentNode.insertBefore(scriptElement, vizElement);
    </script>
    """

    # "<script type='text/javascript'>                    " \
    #     "var divElement = document.getElementById('viz1744217560400');                    " \
    #     "var vizElement = divElement.getElementsByTagName('object')[0];                    " \
    #     "if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1520px';vizElement.style.height='810px';}" \
    #     "else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1520px';vizElement.style.height='810px';}" \
    #     "else { vizElement.style.width='100%';vizElement.style.height='1450px';}                     " \
    #     "" \
    #     "var scriptElement = document.createElement('script');                    " \
    #     "scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    " \
    #     "vizElement.parentNode.insertBefore(scriptElement, vizElement);                " \
    # "</script>"
    
    components.html(html_temp, width=1620, height=860, scrolling=True)

if __name__ == '__main__':
    main()