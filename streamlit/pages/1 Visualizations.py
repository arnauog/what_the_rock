import streamlit as st
import streamlit.components.v1 as components

st.title("Let's see some graphs in Tableau!")
st.write("You can also see the graphs directly in Tableau public: https://public.tableau.com/app/profile/arnau.orengo/viz/Whattherock/UKmap")
st.markdown("#### There are many tabs, don't just stay on the first one.")
col1, col2 = st.columns([0.2, 0.8])
with col2:
    st.write(":point_down:")
def main():
    html_temp="<div class='tableauPlaceholder' id='viz1741429939013' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Wh&#47;Whattherock&#47;Evolutionofrocksubgenres&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Whattherock&#47;Evolutionofrocksubgenres' /><param name='tabs' value='yes' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Wh&#47;Whattherock&#47;Evolutionofrocksubgenres&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='es-ES' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1741429939013');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1420px';vizElement.style.minHeight='810px';vizElement.style.maxHeight='910px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1420px';vizElement.style.minHeight='810px';vizElement.style.maxHeight='910px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='1250px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"
    components.html(html_temp, width=1420, height=960)

if __name__ == '__main__':
    main()