import streamlit as st
import pandas as pd
import json
import os
import header.tech_econ_data as ted

if not os.path.exists('./.cache'):
    os.makedirs('.cache')

st.markdown('# 一、模型设置(基础版)')

st.markdown('## 1. 基本信息')


st.markdown('## 1. 选择项目类型，决定目标函数')

st.markdown('说明: 项目类型分为两类:(1)一体化项目, 电氢氨醇与需求方一体建设, 一体核算成本收益; (2)独立项目, 电氢氨醇与需求方分开建设, 仅考虑电氢氨醇供给侧的成本收益.')
st.markdown('说明:无专门需求的话,建议选择一体化项目进行全局优化.')

project_primary_type={'一体化项目':'integrated','独立项目':'standalone'}[st.selectbox('选择项目类型',['一体化项目','独立项目'],key='project_primary_type')]
final_product=False

if project_primary_type=='integrated':
    st.markdown('说明: 一体化项目中，根据是否考虑对外销售的收益，可以把目标函数分为成本最小化或净收益最大化.')
    main_obj={
    "面向固定需求、固定价格,最大化净收益":'maxnpv',
    "面向固定需求,最小化成本":'maxnpv',
    }[st.selectbox('选择目标函数',['面向固定需求、固定价格,最大化净收益','面向固定需求,最小化成本'],key='integrated_main_obj')]
elif project_primary_type=='standalone':
    st.markdown('说明: 独立项目，需要在绿氢、绿氨、绿醇中选定一种最终供应产品，有多种目标函数可选: (1)给定最小内部收益率,求最小供应价格; (2)给定固定风光资源、最小内部收益率,最大化产品年供应量; (3)给定固定风光资源、固定销售价格,最大化产品年供应量.')

    final_product={'绿氢':'h2','绿氨':'nh3','绿甲醇':'ch3oh'}[st.selectbox('选择最终产品',['绿氢','绿氨','绿甲醇'],key='final_product')]

    main_obj={
    "给定最小内部收益率,求最小供应价格":'miniprice',
    "给定固定风光资源、最小内部收益率,最大化产品年供应量":'maxsupply',
    "给定固定风光资源、固定销售价格,最大化产品年供应量":'maxsupply',
    }[st.selectbox('选择目标函数',['给定最小内部收益率,求最小供应价格','给定固定风光资源、最小内部收益率,最大化产品年供应量','给定固定风光资源、固定销售价格,最大化产品年供应量'],key='stand_alone_main_obj')]

st.markdown('## 2. 这是一个当地项目还是跨区域项目?')

if_multi_region=st.checkbox('是否要为每个节点设置不同的所属地区?不同地区的电网碳排放强度可设为不同',value=False,key='if_multi_region')

with open('./data/province_city.json', encoding="utf-8") as f:
    province_city_node=json.load(f)

st.markdown('### 2.1. 设置节点')

all_available_techs=ted.all_available_techs

nodes_amount = st.number_input(
    "有多少个节点?至少1个,至多35个。", value=1,min_value=1,max_value=35,format='%d',key='nodes_amount'
)

nodes_info={i:{'name':'%d'%i,'location':'','grid':'','available_tech':['None'],'grid_power_emission_coefficient':0.0} for i in range(nodes_amount)}

if if_multi_region:
    st.markdown('请为每个节点分别选择所属的地区')
    for i in range(nodes_amount):
        c=st.columns([1,3,3,3,3,3])
        c[0].markdown('#### 节点%d'%i)
        nodes_info[i]['name']=c[1].text_input("输入节点名字(最多10字符)", "%d"%i,max_chars=10)
        province_i=c[2].selectbox("选择项目所在省",province_city_node.keys(),key='selected_province_%d'%i)
        city_i=c[3].selectbox("选择项目所在市",province_city_node[province_i].keys(),key='selected_city_%d'%i)
        nodes_info[i]['location']=province_city_node[province_i][city_i]['node']
        nodes_info[i]['grid']=province_city_node[province_i][city_i]['grid']
        nodes_info[i]['grid_power_emission_coefficient']=c[4].number_input("输入节点电网电力碳排放强度(t/MWh,如不考虑该因素,默认为0即可)", value=0.0,min_value=-0.5,max_value=1.2,format='%f',key='nodes_ef%d'%i)
        nodes_info[i]['available_tech']=c[5].multiselect('选择可用技术(可多选)',all_available_techs.keys(),['发电技术-光伏','发电技术-风电'],key='available_tech_%d'%i)
else:
    st.markdown('请选择项目所属的地区')
    province_select=st.selectbox('省',province_city_node.keys(),key='province_select')
    city_select=st.selectbox('市',province_city_node[province_select].keys(),key='city_select')

    grid_ef=st.number_input("输入当地电网电力碳排放强度(t/MWh,如不考虑该因素,默认为0即可)", value=0.0,min_value=-0.5,max_value=1.2,format='%f',key='nodes_ef')
    for i in range(nodes_amount):
        c=st.columns([1,3,5])
        c[0].markdown('#### 节点%d'%i)
        nodes_info[i]['name']=c[1].text_input("输入节点名字(最多10字符)", "%d"%i,max_chars=10)
        nodes_info[i]['location']=province_city_node[province_select][city_select]['node']
        nodes_info[i]['grid']=province_city_node[province_select][city_select]['grid']
        nodes_info[i]['available_tech']=c[2].multiselect('选择可用技术(可多选)',all_available_techs.keys(),['发电技术-光伏','发电技术-风电'],key='available_tech_%d'%i)
        nodes_info[i]['grid_power_emission_coefficient']=grid_ef

st.markdown('### 2.2. 设置项目情况')

project_year=st.number_input(
    "本项目从第一期开始一共多少年?",value=30,min_value=1,max_value=50,
    key='project_year'
)

year_amount=st.number_input(
    "本项目计划分为多少期?(1～10期)",value=1,min_value=1,max_value=10,
    key='year_amount'
)

periods_year=[2020]*year_amount
for i in range(year_amount):
    periods_year[i]=st.number_input('请输入第%d期所代表的年份:'%i,value=periods_year[i-1]+1,min_value=periods_year[i-1],max_value=2070,key='periods_year_%d'%i)

all_project_years=[y+periods_year[0] for y in range(project_year)]

st.markdown('### 2.3. 设置可用传输路径')

available_trans_techs=ted.available_trans_techs

nodes_list=list(range(nodes_amount))

dict_for_trans_input={
    "起点": [],
    "终点": [],
    '距离km':0.0}

for k in ted.available_trans_techs.keys():
    dict_for_trans_input[k]=False

arcs = pd.DataFrame(dict_for_trans_input)

if os.path.exists('.cache/arcs.csv'):
    arcs=pd.read_csv('.cache/arcs.csv',index_col=0)
    if len(arcs) == 0:
        arcs = pd.DataFrame(dict_for_trans_input)
    else:
        for k in ted.available_trans_techs.keys():
            for i in arcs.index:
                if arcs.loc[i,k]=='True':
                    arcs.loc[i,k]=True
                elif arcs.loc[i,k]=='False':
                    arcs.loc[i,k]=False

with st.form(key='add_routes'):
    st.markdown('### 添加传输路线')
    st.markdown('注意:如果输入了两条起止点相同的路线,将只保留最后输入的一条.')
    changed_arcs=st.data_editor(
        arcs,
        column_config={
            "起点": st.column_config.SelectboxColumn('起点',
                help="运输路线的起点",
                width="medium",
                options=nodes_list,
                required=True,
            ),
            "终点": st.column_config.SelectboxColumn('终点',
                help="运输路线的终点",
                width="medium",
                options=nodes_list,
                required=True,
            )
        },
        hide_index=True,num_rows="dynamic",use_container_width=True,key='changed_arcs'
    )

    # Every form must have a submit button.
    submitted = st.form_submit_button("提交")
    if submitted:
        for i in changed_arcs.index:
            if int(changed_arcs.loc[i,'起点'])==int(changed_arcs.loc[i,'终点']):
                print(1)
                st.write('第%d条线路起点和终点相同,已删除.'%i)
                changed_arcs.drop(index=i,inplace=True)
        changed_arcs.to_csv('.cache/arcs.csv')

if os.path.exists('.cache/arcs.csv'):
    arcs=pd.read_csv('.cache/arcs.csv',index_col=0)

arcs_info={'%d-%d'%(int(arcs.loc[i,'起点']),int(arcs.loc[i,'终点'])):float(arcs.loc[i,'距离km']) for i in arcs.index}

node_available_tech_constraint={t:[] for t in all_available_techs.values()}

for t in all_available_techs.values():
    for n in nodes_info.keys():
        if len(nodes_info[n]['available_tech'])==0:
            continue
        for at in nodes_info[n]['available_tech']:
            if at == 'None':
                continue
            else:
                if all_available_techs[at]==t:
                    node_available_tech_constraint[t].append(n)

arc_available_trans_constraint={t:[] for t in available_trans_techs.values()}

for t in available_trans_techs.values():
    for i in arcs.index:
        for tr in available_trans_techs.keys():
            if str(available_trans_techs[tr])==str(t) and arcs.loc[i,tr]==True:
                arc_available_trans_constraint[t].append('%d-%d'%(int(arcs.loc[i,'起点']),int(arcs.loc[i,'终点'])))

want_to_check=st.checkbox('检查一下传输和可用技术信息')

if want_to_check:
    st.markdown('### (1) 传输线路信息')
    st.dataframe(arcs_info)

    st.markdown('### (2) 各节点可用技术约束检查')
    for t in node_available_tech_constraint.keys():
        st.markdown('%s可用地点有%s'%(str(t),str(node_available_tech_constraint[t])))

    st.markdown('### (3) 各路径可用技术约束检查')
    for a in arc_available_trans_constraint.keys():
        st.markdown('可以建设%s的路线有%s:'%(str(a),str(arc_available_trans_constraint[a])))

st.markdown('## 3. 输入各种技术的装机总量和需求量约束')
st.markdown('说明:此处的装机总量约束用于某一技术在所有地点的总规模约束,比如本项目只有100MW光伏指标,即光需要将光伏的最大装机容量设为100MW.')

tech_max={y:{} for y in periods_year}

tech_min={y:{} for y in periods_year}

for t in list(node_available_tech_constraint.keys())[:-ted.consume_type_amount]:
    col_3=st.columns([1]*(1+3*len(periods_year)))
    col_3[0].markdown('#### %s:'%t)
    for k in range(len(periods_year)):
        check_caplimit=col_3[k*3+1].checkbox("%d年是否有容量约束?"%periods_year[k],value=False,key='capacity_limit_%s_%d'%(t,periods_year[k]))
        maxcap=col_3[k*3+2].number_input("%d年最大装机量"%periods_year[k], value=0,key='maxcap_%s_%d'%(t,periods_year[k]))
        mincap=col_3[k*3+3].number_input("%d年最小装机量"%periods_year[k], value=0,key='mincap_%s_%d'%(t,periods_year[k]))
        if check_caplimit:
            tech_max[periods_year[k]][t]=maxcap
            tech_min[periods_year[k]][t]=mincap

def create_dem_template(node_available_tech_constraint):
    power_dem_hourfix=pd.DataFrame(0.0,index=range(8760),columns=['unit']+['%s-%s'%(n,y) for n in node_available_tech_constraint['PD-hourfix'] for y in periods_year])

    power_dem_hourfix.loc[:,'unit']='MWh'

    h2_dem_hourfix=pd.DataFrame(0.0,index=range(8760),columns=['unit']+['%s-%s'%(n,y) for n in node_available_tech_constraint['HD-hourfix'] for y in periods_year])

    h2_dem_hourfix.loc[:,'unit']='t'

    nh3_dem_hourfix=pd.DataFrame(0.0,index=range(8760),columns=['unit']+['%s-%s'%(n,y) for n in node_available_tech_constraint['AD-hourfix'] for y in periods_year])

    nh3_dem_hourfix.loc[:,'unit']='t'

    ch3oh_dem_hourfix=pd.DataFrame(0.0,index=range(8760),columns=['unit']+['%s-%s'%(n,y) for n in node_available_tech_constraint['MD-hourfix'] for y in periods_year])

    ch3oh_dem_hourfix.loc[:,'unit']='t'

    power_dem_shiftable=pd.DataFrame(0.0,index=range(365),columns=['unit']+['%s-%s'%(n,y) for n in node_available_tech_constraint['PD-dayfix'] for y in periods_year])

    power_dem_shiftable.loc[:,'unit']='MWh'

    h2_dem_shiftable=pd.DataFrame(0.0,index=range(365),columns=['unit']+['%s-%s'%(n,y) for n in node_available_tech_constraint['HD-dayfix'] for y in periods_year])

    h2_dem_shiftable.loc[:,'unit']='t'

    nh3_dem_shiftable=pd.DataFrame(0.0,index=range(365),columns=['unit']+['%s-%s'%(n,y) for n in node_available_tech_constraint['AD-dayfix'] for y in periods_year])

    nh3_dem_shiftable.loc[:,'unit']='t'

    ch3oh_dem_shiftable=pd.DataFrame(0.0,index=range(365),columns=['unit']+['%s-%s'%(n,y) for n in node_available_tech_constraint['MD-dayfix'] for y in periods_year])

    ch3oh_dem_shiftable.loc[:,'unit']='t'

    have_dem_locations=list(set(node_available_tech_constraint['PD-hourfix']+ node_available_tech_constraint['HD-hourfix']+ node_available_tech_constraint['AD-hourfix']+ node_available_tech_constraint['PD-dayfix']+ node_available_tech_constraint['HD-dayfix']+ node_available_tech_constraint['AD-dayfix']+ node_available_tech_constraint['MD-dayfix']+ node_available_tech_constraint['MD-dayfix']))

    shiftable_dem_info=pd.DataFrame(0.0,index=['%s-%s'%(t,f) for t in ['PD','HD','AD','MD'] for f in ['HourMax','HourMin']],columns=['%s-%s'%(n,y) for n in have_dem_locations for y in periods_year])

    with pd.ExcelWriter('.cache/DemandDataTemplate.xlsx') as w:
        power_dem_hourfix.to_excel(w,sheet_name='小时固定的电力需求')
        h2_dem_hourfix.to_excel(w,sheet_name='小时固定的氢需求')
        nh3_dem_hourfix.to_excel(w,sheet_name='小时固定的氨需求')
        ch3oh_dem_hourfix.to_excel(w,sheet_name='小时固定的甲醇需求')
        power_dem_shiftable.to_excel(w,sheet_name='日内可调节的电力需求')
        h2_dem_shiftable.to_excel(w,sheet_name='日内可调节的氢需求')
        nh3_dem_shiftable.to_excel(w,sheet_name='日内可调节的氨需求')
        ch3oh_dem_shiftable.to_excel(w,sheet_name='日内可调节的甲醇需求')
        shiftable_dem_info.to_excel(w,sheet_name='日内可调节需求的参数')

    dict_DemandDataTemplate={'power_dem_hourfix':power_dem_hourfix,'h2_dem_hourfix':h2_dem_hourfix,'nh3_dem_hourfix':nh3_dem_hourfix,'ch3oh_dem_hourfix':ch3oh_dem_hourfix,'power_dem_shiftable':power_dem_shiftable,'h2_dem_shiftable':h2_dem_shiftable,'nh3_dem_shiftable':nh3_dem_shiftable,'ch3oh_dem_shiftable':ch3oh_dem_shiftable,'shiftable_dem_info':shiftable_dem_info}
    return dict_DemandDataTemplate

dict_DemandDataTemplate=create_dem_template(node_available_tech_constraint)

st.markdown('### 输入电氢氨醇需求数据')

def input_dem_data(which_dem='PD'):
    dem_name={'PD':'电力','HD':'氢','AD':'氨','MD':'醇'}
    dem_name_en={'PD':'power','HD':'h2','AD':'nh3','MD':'ch3oh'}
    dem_name_unit={'PD':'MWh','HD':'t','AD':'t','MD':'t'}
    if len(node_available_tech_constraint['%s-dayfix'%which_dem])+len(node_available_tech_constraint['%s-hourfix'%which_dem])>0:
        st.markdown('#### 输入%s需求数据'%dem_name[which_dem])
        dem_col=st.columns([1]*(len(periods_year)))

        annual_demand=pd.DataFrame(0.0,index=['%d-dayfix'%n for n in node_available_tech_constraint['%s-dayfix'%which_dem]]+['%d-hourfix'%n for n in node_available_tech_constraint['%s-hourfix'%which_dem]],columns=periods_year)

        for k in range(len(periods_year)):
            for n in annual_demand.index:
                annual_demand.loc[n,periods_year[k]]=dem_col[k].number_input("请输入%d年节点%s,%s年度总需求(单位:%s)"%(periods_year[k],n,dem_name[which_dem],dem_name_unit[which_dem]), value=0.0,key='%s_annual_demand_%d_%s'%(which_dem,periods_year[k],n))

        for n in annual_demand.index:
            node_number=int(n.split('-')[0])
            node_dem_type=n.split('-')[1]
            if node_dem_type == 'hourfix':
                for y in periods_year:
                    dict_DemandDataTemplate['%s_dem_hourfix'%dem_name_en[which_dem]].loc[:,'%s-%s'%(node_number,y)]=annual_demand.loc[n,y]/8760.0
            elif node_dem_type == 'dayfix':
                for y in periods_year:
                    dict_DemandDataTemplate['%s_dem_hourfix'%dem_name_en[which_dem]].loc[:,'%s-%s'%(node_number,y)]=annual_demand.loc[n,y]/365.0
                    dict_DemandDataTemplate['shiftable_dem_info'].loc['%s-HourMax'%which_dem,'%s-%s'%(node_number,y)]=annual_demand.loc[n,y]/365.0
                    dict_DemandDataTemplate['shiftable_dem_info'].loc['%s-HourMin'%which_dem,'%s-%s'%(node_number,y)]=0.0

input_dem_data('PD')
input_dem_data('HD')
input_dem_data('AD')
input_dem_data('MD')

st.markdown('## 4. 输入模型主要参数')

technical_max_coal_ammonia_ratio=st.number_input("输入煤电机组最大掺氨比例(若不考虑,默认为0即可)", value=0.0, min_value=0.0,max_value=0.4,key='technical_max_coal_ammonia_ratio')

annual_coal_ammonia_ratio=st.number_input("输入煤电年度总体最低掺氨比例(若不考虑,默认为0即可)", value=0.0, min_value=0.0,max_value=1.0,key='annual_coal_ammonia_ratio')

coal_power_max_hour=st.number_input("输入煤电最大利用小时数(若不考虑,默认为8760即可)", value=8760, min_value=0,max_value=8760,key='coal_power_max_hour')

discounted_rate=0.06
grid_power_scenario={y:0.2 for y in periods_year}
sell_power_scenario={y:False for y in periods_year}
carbon_price={y:0.0 for y in periods_year}

discounted_rate = st.number_input("输入折现率", value=0.06,min_value=0.0,max_value=1.0,key='discounted_rate')

for y in periods_year:
    grid_power_scenario[y] = st.number_input("输入%d年的最大购电比率(下网电量占总用电量比例)"%y, value=0.20,min_value=0.0,max_value=1.0,key='grid_power_scenario_%d'%y)

allow_sell_pu=st.checkbox("是否允许售电到电网?",key='allow_sell_pu')

if_swap_buy_sell=0
if_swap_month_meet=0
fixed_sell_power_price={n:{y:pd.Series(0.0,index=range(8760)).to_dict() for y in periods_year} for n in nodes_info.keys()}


def create_sell_power_price_template(nodes,years):
    with pd.ExcelWriter('.cache/sell_electricity_price.xlsx') as w:
        for n in nodes:
            pd.DataFrame(0.0,index=range(8760),columns=years).to_excel(w,sheet_name='节点%s的分年分小时电价'%n)

if allow_sell_pu:
    for y in periods_year:
        sell_power_scenario[y] = st.number_input("输入%d年的最大售电比率(上网电量占总发电量比例)"%y, value=0.20,min_value=0.0,max_value=1.0,key='sell_power_scenario_%d'%y)

    if st.checkbox("是否采取年度的与项目电网电量交换?(卖电不收钱, 买电不交电量电费, 但要交变压器容量电费和最大需求量电费, 每年的买卖电量要相等)",key='if_swap_buy_sell'):
        if_swap_buy_sell=1
        if st.checkbox("是否进一步把每年的买卖电量相等改为每月相等)",key='if_swap_month_meet'):
            if_swap_month_meet=1
    else:
        st.markdown('输入外生确定的各个节点的售电价格')
        if st.checkbox("设为全年统一的固定电价",value=True,key='if_fix_sell_power_price'):
            sell_electricity_price_df=pd.DataFrame(0.0,index=nodes_info.keys(),columns=periods_year)
            sell_electricity_price_df=st.data_editor(sell_electricity_price_df,key='change_sell_electricity_price_df')
            for n in nodes_info.keys():
                for y in periods_year:
                    fixed_sell_power_price[n][y]=pd.Series(sell_electricity_price_df.loc[n,str(y)],index=range(8760)).to_dict()
        else:
            with st.container():
                st.markdown('请通过模板文件修改各个节点、各年份、各小时的售电电价。请仅修改模板文件中的电价数字(单位为元/kWh).')
                create_sell_power_price_template(nodes_info.keys(),periods_year)
                with open("./.cache/sell_electricity_price.xlsx", "rb") as file:
                    btn = st.download_button(
                        label="下载各个节点、各年份、各小时的售电电价的输入模板",
                        data=file,
                        file_name="售电电价数据模版.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key='down_sell_electricity_price_template'
                    )

                uploaded_price_file = st.file_uploader(
                    "请上传填写好的模板", accept_multiple_files=False,key='up_sell_electricity_price_template'
                )

                if uploaded_price_file is not None:
                    with pd.ExcelFile(uploaded_price_file) as w:
                        for n in nodes_info.keys():
                            df=pd.read_excel(w,sheet_name='节点%s的分年分小时电价'%n,index_col=0)
                            for y in periods_year:
                                fixed_sell_power_price[n][y]=df[y].to_dict()

st.markdown('输入外生确定的碳市场价格')
for y in periods_year:
    carbon_price[y]=st.number_input("输入%d年的碳价格(千元/吨)"%y, value=0.1,min_value=0.00,key='carbon_price_%d'%y)


st.markdown('## 5. 选择关键约束')

st.markdown('### (1) 项目内部收益率约束')
st.markdown('项目的内部收益率约束是针对整个项目的生命周期的, 并不针对某一具体年份或某一期。特别的, 如果有最低内部收益率约束, 则之前输入的折现率无效.')

if_fix_IRR=st.checkbox("是否有最低内部收益率要求?",key='if_fix_IRR')

fix_IRR=discounted_rate

if if_fix_IRR:
    fix_IRR=st.number_input("输入固定内部收益率(小数形式)", value=0.06,min_value=0.0,max_value=1.0,key='fix_IRR')

st.markdown('### (2) 项目氢、氨、甲醇供应范围约束')

if_sell_h2=st.checkbox("是否能不限时间地点自由向氢市场售氢?(即该项目为开放性项目, 可以向项目之外的不定需求供氢)",key='if_sell_h2')

if_lower_free_h2_supply=st.checkbox("是否有全年开放售氢最小总量的约束?(不限时间地点自由向氢市场售出的氢)",key='if_lower_free_h2_supply')

lower_free_h2_supply=pd.Series(0.0,index=periods_year)

if if_lower_free_h2_supply:
    for y in periods_year:
        lower_free_h2_supply.loc[y]=st.number_input("输入%d年的除固定需求外开放售氢最小总量"%y, value=0.0,min_value=0.0,key='lower_free_h2_supply_%d'%y)

if_sell_nh3=st.checkbox("是否能不限时间地点自由向氨市场售氨?",key='if_sell_nh3')

if_lower_free_nh3_supply=st.checkbox("是否有全年开放售氨最小总量的约束?",key='if_lower_free_nh3_supply')

lower_free_nh3_supply=pd.Series(0.0,index=periods_year)

if if_lower_free_nh3_supply:
    for y in periods_year:
        lower_free_nh3_supply.loc[y]=st.number_input("输入%d年的除固定需求外开放售氨最小总量"%y, value=0.0,min_value=0.0,key='lower_free_nh3_supply_%d'%y)

if_sell_ch3oh=st.checkbox("是否能不限时间地点自由向甲醇市场售甲醇?",key='if_sell_ch3oh')

if_lower_free_ch3oh_supply=st.checkbox("是否有全年开放售甲醇最小总量的约束?",key='if_lower_free_ch3oh_supply')

lower_free_ch3oh_supply=pd.Series(0.0,index=periods_year)

if if_lower_free_ch3oh_supply:
    for y in periods_year:
        lower_free_ch3oh_supply.loc[y]=st.number_input("输入%d年的除固定需求外开放售甲醇最小总量"%y, value=0.0,min_value=0.0,key='lower_free_ch3oh_supply_%d'%y)

st.markdown('### (3) 项目氢、氨、甲醇供应价格约束')

if_fix_node_h2_price=st.checkbox("固定需求氢是否有固定氢价格?",key='if_fix_node_h2_price')

fix_node_h2_price=pd.DataFrame(20.0,index=periods_year,columns=list(set(node_available_tech_constraint['HD-hourfix']+node_available_tech_constraint['HD-dayfix'])))

fix_sell_h2_price=pd.Series(30.0,index=periods_year)

if if_fix_node_h2_price:
    st.markdown('**请输入项目周期内各节点各时间内部氢价(千元/吨),氢价可以各节点各年不同。**')
    fix_node_h2_price=st.data_editor(
        fix_node_h2_price,
        hide_index=False,num_rows="fixed",use_container_width=True,key='fix_node_h2_price')

if if_sell_h2:
    st.markdown('**请输入项目周期内向外部售氢的固定氢价(千元/吨), 可以各年不同。**')
    fix_sell_h2_price=st.data_editor(
        fix_sell_h2_price,
        hide_index=False,num_rows="fixed",use_container_width=True,key='fix_sell_h2_price')

if_fix_node_nh3_price=st.checkbox("固定需求氢是否有固定氨价格?",key='if_fix_node_nh3_price')

fix_node_nh3_price=pd.DataFrame(20.0,index=periods_year,columns=list(set(node_available_tech_constraint['AD-hourfix']+node_available_tech_constraint['AD-dayfix'])))

fix_sell_nh3_price=pd.Series(30.0,index=periods_year)

if if_fix_node_nh3_price:
    st.markdown('**请输入项目周期内各节点各时间内部氨价(千元/吨),氨价可以各节点各年不同。**')
    fix_node_nh3_price=st.data_editor(
        fix_node_nh3_price,
        hide_index=False,num_rows="fixed",use_container_width=True,key='fix_node_nh3_price')

if if_sell_nh3:
    st.markdown('**请输入项目周期内向外部售氨的固定氨价(千元/吨), 可以各年不同。**')
    fix_sell_nh3_price=st.data_editor(
        fix_sell_nh3_price,
        hide_index=False,num_rows="fixed",use_container_width=True,key='fix_sell_nh3_price')

if_fix_node_ch3oh_price=st.checkbox("固定需求氢是否有固定甲醇价格?",key='if_fix_node_ch3oh_price')

fix_node_ch3oh_price=pd.DataFrame(20.0,index=periods_year,columns=list(set(node_available_tech_constraint['MD-hourfix']+node_available_tech_constraint['MD-dayfix'])))

fix_sell_ch3oh_price=pd.Series(30.0,index=periods_year)

if if_fix_node_ch3oh_price:
    st.markdown('**请输入项目周期内各节点各时间内部甲醇价(千元/吨),甲醇价可以各节点各年不同。**')
    fix_node_ch3oh_price=st.data_editor(
        fix_node_ch3oh_price,
        hide_index=False,num_rows="fixed",use_container_width=True,key='fix_node_ch3oh_price')

if if_sell_ch3oh:
    st.markdown('**请输入项目周期内向外部售甲醇的固定甲醇价(千元/吨), 可以各年不同。**')
    fix_sell_ch3oh_price=st.data_editor(
        fix_sell_ch3oh_price,
        hide_index=False,num_rows="fixed",use_container_width=True,key='fix_sell_ch3oh_price')

st.markdown('### (4) 特殊约束')

st.markdown('#### 各期最大总风光资源量总和约束(若不需要单独为各期设置指标, 可以令每一期该约束都相等, 即为针对该项目总体的约束)')

if_fix_re_capacity=st.checkbox("是否有风光总量的约束?",key='if_fix_re_capacity')

fix_re_capacity=pd.Series(0.0,index=periods_year)
if if_fix_re_capacity:
    for y in periods_year:
        fix_re_capacity.loc[y]=st.number_input("输入%d年的最大风光资源量总和(MW)"%y, value=100.0,min_value=0.0,key='fix_re_capacity_%d'%y)

st.markdown('## 6. 各类技术参数修改')

techecon_data=ted.read_techecon_data(periods_year)

if st.checkbox('是否需要修改各类技术参数?',key='revise_tech'):
    st.markdown('### 技术英文缩写对照如下')
    st.write(all_available_techs)
    st.write(available_trans_techs)

    st.markdown('### (6.1) 固定成本参数修改')
    if st.checkbox('是否需要修改技术的固定成本',key='revise_fixcost'):
        st.markdown('**注意:** 几类储能技术有不同的容量/功率比(储能时长),默认数据下,ES_Li为2小时锂电池储能,ES_FR为4小时液流储能,HS为5小时储氢罐,AS为1小时储氨罐')
        for t in techecon_data.keys():
            if st.checkbox('是否修改%s?'%t,key='revise_%s'%t):
                techecon_data[t]['unit']['cap']=st.number_input('请修改单个%s设备的容量, 默认为%f, 单位为%s'%(t,techecon_data[t]['unit']['cap'],techecon_data[t]['unit']['cap_unit']),value=float(techecon_data[t]['unit']['cap']),key='number_input_unit_cap_%s'%t,format='%.5f')
                for y in periods_year:
                    techecon_data[t]['unit']['fixed_cost'][y]=st.number_input('请修改单个%s设备在%s年的固定购置成本, 默认为%f, 单位为%s'%(t,y,techecon_data[t]['unit']['fixed_cost'][y],techecon_data[t]['unit']['fixed_cost_unit']),value=float(techecon_data[t]['unit']['fixed_cost'][y]),min_value=0.0,key='number_input_unit_fixcost_%s_%s'%(t,y),format='%.5f')

    st.markdown('### (6.2) 技术的运维成本修改')
    if st.checkbox('是否需要修改技术的运维成本',key='revise_omc'):
        for t in techecon_data.keys():
            if st.checkbox('是否修改%s的运维成本占总投资成本的比例?'%t,key='revise_OMC_%s'%t):
                techecon_data[t]['unit']['OMC_rate']=st.number_input('请修改%s的运维成本占总投资成本的比例,默认为%f.'%(t,techecon_data[t]['unit']['OMC_rate']),value=techecon_data[t]['unit']['OMC_rate'],key='number_input_OMC_%s'%t,format='%.4f')

    st.markdown('### (6.3) 技术的寿命修改')
    if st.checkbox('是否需要修改技术的寿命',key='revise_life'):
        for t in techecon_data.keys():
            if st.checkbox('是否修改%s的寿命?'%t,key='revise_life_%s'%t):
                techecon_data[t]['unit']['life']=st.number_input('请修改%s的寿命,默认为%d.'%(t,techecon_data[t]['unit']['life']),value=techecon_data[t]['unit']['life'],key='number_input_life_%s'%t)

    st.markdown('### (6.4) 设备技术参数修改')
    if st.checkbox('是否需要修改技术的技术参数',key='revise_tech_parameter'):
        for t in techecon_data.keys():
            if len(techecon_data[t]['coef'])>0:
                if st.checkbox('是否修改%s的技术参数?'%t,key='revise_tech_parameter_%s'%t):
                    for k in techecon_data[t]['coef'].keys():
                        if type(techecon_data[t]['coef'][k]) == int or type(techecon_data[t]['coef'][k]) == float:
                            techecon_data[t]['coef'][k]=st.number_input('请修改%s的%s,默认为%f.'%(t,k,techecon_data[t]['coef'][k]),value=float(techecon_data[t]['coef'][k]),key='revise_%s_%s'%(t,k),format='%.5f')
                        elif type(techecon_data[t]['coef'][k]) == dict:
                            if len(techecon_data[t]['coef'][k])<11:
                                for k2 in techecon_data[t]['coef'][k].keys():
                                    techecon_data[t]['coef'][k][k2]=st.number_input('请修改%s,%s的%s参数,默认为%f.'%(t,k,k2,techecon_data[t]['coef'][k][k2]),value=float(techecon_data[t]['coef'][k][k2]),key='revise_%s_%s_%s'%(t,k,k2),format='%.5f')
                            else:
                                st.markdown('请修改%s的%s参数:'%(t,k))
                                st.data_editor(techecon_data[t]['coef'][k])

st.markdown('## 7. 生成模型参数文件')

model_name=st.text_input("输入模型名称:", "default")

st.markdown('模型名称为%s'%model_name)

try:
    input_coef={
        'model_name':model_name,
        'periods_year':periods_year,
        'all_project_years':all_project_years,
        'project_primary_type':project_primary_type,
        'final_product':final_product,
        'objective':main_obj,
        'nodes_info':nodes_info,
        'arcs_info':arcs_info,
        'node_available_tech_constraint':node_available_tech_constraint,
        'arc_available_trans_constraint':arc_available_trans_constraint,
        'tech_max':tech_max,
        'tech_min':tech_min,
        'discounted_rate':discounted_rate,
        'grid_power_scenario':grid_power_scenario,
        'sell_power_scenario':sell_power_scenario,
        'allow_sell_pu':allow_sell_pu,
        'fixed_sell_power_price':fixed_sell_power_price,
        'if_fix_IRR':if_fix_IRR,
        'fix_IRR':fix_IRR,
        'if_sell_h2':if_sell_h2,
        'if_lower_free_h2_supply':if_lower_free_h2_supply,
        'lower_free_h2_supply':lower_free_h2_supply.to_dict(),
        'if_sell_nh3':if_sell_nh3,
        'if_lower_free_nh3_supply':if_lower_free_nh3_supply,
        'lower_free_nh3_supply':lower_free_nh3_supply.to_dict(),
        'if_sell_ch3oh':if_sell_ch3oh,
        'if_lower_free_ch3oh_supply':if_lower_free_ch3oh_supply,
        'lower_free_ch3oh_supply':lower_free_ch3oh_supply.to_dict(),
        'if_fix_node_h2_price':if_fix_node_h2_price,
        'fix_node_h2_price':fix_node_h2_price.to_dict(),
        'fix_sell_h2_price':fix_sell_h2_price.to_dict(),
        'if_fix_node_nh3_price':if_fix_node_nh3_price,
        'fix_node_nh3_price':fix_node_nh3_price.to_dict(),
        'fix_sell_nh3_price':fix_sell_nh3_price.to_dict(),
        'if_fix_node_ch3oh_price':if_fix_node_ch3oh_price,
        'fix_node_ch3oh_price':fix_node_ch3oh_price.to_dict(),
        'fix_sell_ch3oh_price':fix_sell_ch3oh_price.to_dict(),
        'if_fix_re_capacity':if_fix_re_capacity,
        'fix_re_capacity':fix_re_capacity.to_dict(),
        'if_swap_buy_sell':if_swap_buy_sell,
        'if_swap_month_meet':if_swap_month_meet,
        'techecon_data':techecon_data,
        'carbon_price':carbon_price,
        'technical_max_coal_ammonia_ratio':technical_max_coal_ammonia_ratio,
        'annual_coal_ammonia_ratio':annual_coal_ammonia_ratio,
        'coal_power_max_hour':coal_power_max_hour,
        'power_dem_hourfix':dict_DemandDataTemplate['power_dem_hourfix'].to_dict(),
        'h2_dem_hourfix':dict_DemandDataTemplate['h2_dem_hourfix'].to_dict(),
        'nh3_dem_hourfix':dict_DemandDataTemplate['nh3_dem_hourfix'].to_dict(),
        'ch3oh_dem_hourfix':dict_DemandDataTemplate['ch3oh_dem_hourfix'].to_dict(),
        'power_dem_shiftable':dict_DemandDataTemplate['power_dem_shiftable'].to_dict(),
        'h2_dem_shiftable':dict_DemandDataTemplate['h2_dem_shiftable'].to_dict(),
        'nh3_dem_shiftable':dict_DemandDataTemplate['nh3_dem_shiftable'].to_dict(),
        'ch3oh_dem_shiftable':dict_DemandDataTemplate['ch3oh_dem_shiftable'].to_dict(),
        'shiftable_dem_info':dict_DemandDataTemplate['shiftable_dem_info'].to_dict()}

    with open('./.cache/modelinput.json','w',encoding="utf-8") as file:
        json.dump(input_coef,file,indent=4,ensure_ascii=False)

    with open('./.cache/modelinput.json','r',encoding="utf-8") as file:
        btn = st.download_button(
            label="下载已生成模型参数文件",
            data=file,
            file_name="modelinput.json",
            mime="text/json",
            key='input_coef'
            )

except:
    st.markdown('数据还没有输入完整, 请按顺序执行！')