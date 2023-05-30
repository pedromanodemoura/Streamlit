# -*- coding: utf-8 -*-
"""
Created on Mon May  8 11:14:53 2023

@author: c20460
"""

import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import random, string
import json
import pyperclip


url = 'https://medium.com/_/graphql'

with open('docs/medium_article_query.txt') as t:
    query = t.read()

with open('docs/medium_article_graphql.txt', encoding='utf-8') as t:
    body_str = t.read()


def get_article(title):
    
    post_id = title.split('-')[-1]

    uuid = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    headers = {
        'origin': 'https://medium.com',
        'referer': 'https://medium.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'ot-tracer-spanid': '24330eb165f5d5c2',
        'ot-tracer-traceid': '607cd535383d11a6',
        'cookie': f'__cfruid=b5fe07e746a9a7ae1abfeedc598d708ac3bcec62-1684157859; _ga=GA1.2.289975943.1684159338; _gid=GA1.2.565438714.1684159338; lightstep_guid/medium-web=f624200ec15101g; lightstep_session_id=5eba377b3cea551c; sz=1903; pr=1; tz=240; xsrf=pcRGPUuunAfndUT8; nonce=gUL4qgU1; uid={uuid}; sid=1:48mW1ks+sOFDhC2lJskz2gCNDxIanS/caaug0RN4cGLNJxQzy8DMkl3GGPWlXWJA; dd_cookie_test_b47573b6-79f4-4fcd-aadc-b20b2d46982f=test; _dd_s=rum=0&expire=1684160903889; dd_cookie_test_992fd195-1e22-40a1-8c1d-3ceb4b56d6fe=test'
        }
    
    variables = {"postId": post_id,
                 "postMeteringOptions":{
                     "referrer":""
                     }
                 }
    
    r = requests.request("POST", url, headers=headers, json={'query': query, "variables": variables})
    
    df = pd.json_normalize(r.json()['data']['post']['viewerEdge']['fullContent']['bodyModel']['paragraphs'])
    
    full_str = ''
    
    post_loc = '/'.join(title.split('/')[:3])+ '/media/'
    
    for i in range(len(df)):
        if df.loc[i,'type'] == "IMG":
            part_2 = f"""<{df.loc[i,'type']} id="{df.loc[i,'name']}" alt="" class="bg oe of c nr ns nt oa ob ff oc bg od nu nv nw nx ny nz nr ns paragraph-image" width="700" height="499" loading="eager" role="presentation" src="https://miro.medium.com/v2/resize:fit:700/{df.loc[i,'metadata.id']}">"""
        elif df.loc[i,'type'] == "PRE":
            part_2 = f"""<SPAN id="{df.loc[i,'name']}" class="ra op gq qf b bf rb rc l rd re nu nv nw nx ny qv qf qw bo qx qy qz"> {df.loc[i,'text']}</SPAN>"""
        elif df.loc[i,'type'] == "H3":
            part_2 = f"""<H1 id="{df.loc[i,'name']}" class="pw-post-title fm fn fo be fp fq fr fs ft fu fv fw fx fy fz ga gb gc gd ge gf gg gh gi gj gk bj"> {df.loc[i,'text']}</H1>"""
        elif df.loc[i,'type'] == "H4":
            part_2 = f"""<H2 id="{df.loc[i,'name']}" class="pw-subtitle-paragraph gl fn fo be b gm gn go gp gq gr gs gt gu gv gw gx gy gz ha cp dv"> {df.loc[i,'text']}</H2>"""
        elif df.loc[i,'type'] == "ULI":
            part_2 = f"""<LI id="{df.loc[i,'name']}" class="ms mt gq mu b mv mw mx my mz na nb nc pr ne nf ng ps ni nj nk pt nm nn no np pu pv pw bj"> {df.loc[i,'text']}</LI>"""
        elif df.loc[i,'type'] == "OLI":
            part_2 = f"""<LI id="{df.loc[i,'name']}" class="na nb fo nc b gm pt ne nf gp pu nh ni pk pv nl nm pl pw np nq pm px nt nu nv pn po pp bj"> {df.loc[i,'text']}</LI>"""
        elif df.loc[i,'type'] == "IFRAME":
            media_loc = post_loc if df.loc[i,'iframe.mediaResource.iframeSrc'] == '' else df.loc[i,'iframe.mediaResource.iframeSrc']
            width = "100%" if df.loc[i,'iframe.mediaResource.iframeWidth'] == 0 else df.loc[i,'iframe.mediaResource.iframeWidth']
            part_2 = f"""<IFRAME onload="resizeIframe(this)" "scrolling="no" height="{df.loc[i,'iframe.mediaResource.iframeHeight']}" width="{width}" id="{df.loc[i,'name']}" src="{media_loc}{df.loc[i,'iframe.mediaResource.id']}" class="ek n fc dx bg pt is l eb"> </IFRAME>"""
        else:
            part_2 = f"""<{df.loc[i,'type']} id="{df.loc[i,'name']}" class="pw-post-body-paragraph ms mt gq mu b mv mw mx my mz na nb nc nd ne nf ng nh ni nj nk nl nm nn no np gj bj"> {df.loc[i,'text']}</{df.loc[i,'type']}>"""
     
        part_2 = part_2.replace('\n', '<br>')
    
        full_str += "<br>" + part_2
        
    title = df.query("type in ('H3')").reset_index().loc[0,'text']
        
    return full_str, title

css = """<style>
.re{
    min-width: fit-content;    
}
.rd {
    white-space: pre;
}
.rc {
    margin-bottom: -0.2em;
}
.rb {
    margin-top: -0.2em;
}
.ra {
    line-height: 1.4;
}
.qf {
    font-family: source-code-pro, Menlo, Monaco, "Courier New", Courier, monospace;
}
.op {
    letter-spacing: -0.022em;
}
.gq {
    font-style: normal;
}
.bf {
    font-size: 14px;
}
.l {
    display: block;
}
.b {
    font-weight: 400;
}
.qz {
    color: #242424;
}
.gk {
    word-wrap: break-word;
}

.gj {
    word-break: break-word;
}
.ny {
    margin-top: 56px;
}
.qz {
    color: #242424;
}
.qy {
    background: #F9F9F9;
}
.qx {
    border: 1px solid #E5E5E5;
}
.qw {
    padding: 32px;
}
.qv {
    overflow-x: auto;
}
.qf {
    font-family: source-code-pro, Menlo, Monaco, "Courier New", Courier, monospace;
}
.bo {
    border-radius: 4px;
}
.pt {
    font-size: 21px;
}
media="(min-width: 1080px)"
.no {
    letter-spacing: -0.003em;
}
media="(min-width: 1080px)"
.nn {
    line-height: 32px;
}
media="(min-width: 1080px)"
.nm {
    margin-top: 2em;
}
.pw {
    padding-left: 0px;
}
.pv {
    margin-left: 30px;
}
.pu {
    list-style-type: disc;
}
.np {
    margin-bottom: -0.46em;
}
.mu {
    font-family: source-serif-pro, Georgia, Cambria, "Times New Roman", Times, serif;
}
.mt {
    letter-spacing: -0.004em;
}
.ms {
    line-height: 1.58;
}
.gq {
    font-style: normal;
}
.bj {
    color: rgba(41, 41, 41, 1);
}
.b {
    font-weight: 400;
li {
    display: list-item;
    text-align: -webkit-match-parent;
}
.gj {
    word-break: break-word;
}
.no {
    letter-spacing: -0.003em;
}
media="(min-width: 1080px)"
.nn {
    line-height: 32px;
}
media="(min-width: 1080px)"
.nm {
    margin-top: 2em;
}
media="(min-width: 1080px)"
.nl {
    font-size: 20px;
}
.np {
    margin-bottom: -0.46em;
}
.mu {
    font-family: source-serif-pro, Georgia, Cambria, "Times New Roman", Times, serif;
}
.mt {
    letter-spacing: -0.004em;
}
.ms {
    line-height: 1.58;
}
.gq {
    font-style: normal;
}
.gj {
    word-break: break-word;
}
.bj {
    color: rgba(41, 41, 41, 1);
}
.b {
    font-weight: 400;
}
h1, h2, h3, h4, h5, h6, dl, dd, ol, ul, menu, figure, blockquote, p, pre, form {
    margin: 0;
}
p {
    display: block;
    margin-block-start: 1em;
    margin-block-end: 1em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
}
.ny {
    margin-top: 56px;
}
.nz {
    clear: both;
}
.ns {
    margin-right: auto;
}
.nr {
    margin-left: auto;
}
figure {
    display: block;
    margin-block-start: 1em;
    margin-block-end: 1em;
    margin-inline-start: 40px;
    margin-inline-end: 40px;
}
.oa {
    transition: transform 300ms cubic-bezier(0.2, 0, 0.2, 1);
}

.oc {
    z-index: auto;
}
.ob {
    cursor: zoom-in;
}
.ff {
    position: relative;
}
.bg {
    width: 100%;
}
.nt {
    max-width: 1999px;
}

.ns {
    margin-right: auto;
}
.nr {
    margin-left: auto;
}
.of {
    height: auto;
}
.oe {
    max-width: 100%;
}
.bg {
    width: 100%;
}
.c {
    background-color: rgba(255, 255, 255, 1);
}
img, svg {
    vertical-align: middle;
}
fc {
    left: 0;
}
.ek {
    position: absolute;
}
.dx {
    height: 100%;
}
n {
    top: 0;
}
pt {
    margin: auto;
}
.is {
    overflow: hidden;
}
.eb {
    position: relative;
}
</style> 
"""



st.markdown(css, unsafe_allow_html=True)

title = st.text_input('Article ID', '9a0f02b150da')

js = """
function resizeIframe(iframe) {
  iframe.height = iframe.contentWindow.document.body.clientHeight + "px";
}

var frames = document.getElementsByTagName("iframe");

for (i=0; i<frames.length; i++){
  resizeIframe(frames[i]);
}
"""

if st.button('Copy'):
    full_str, post_title = get_article(title) 
    full_str_fixed = full_str.replace('`', "\`").replace("$", "\$")
    copy_str = f"""
        $("html").innerHTML = ""
        $("html").innerHTML = `{css+full_str_fixed}`;
    """ + js
    pyperclip.copy(copy_str)

if st.button('Run'):
    full_str, post_title = get_article(title)
    st.markdown(full_str, unsafe_allow_html=True)
    components.html(js)
    

