import streamlit as st
import pandas as pd
import header.tech_econ_data as ted

st.markdown('# 3.模型结果可视化')

uploaded_model_result = st.file_uploader(
    "请上传模型结果的Excel文件", accept_multiple_files=False,key='uploaded_model_result', type=['xlsx']
    )

@st.cache_data
def read_result_from_file(file):
    with pd.ExcelFile(file) as w:
        output_new_capacity=pd.read_excel(w,sheet_name='new_capacity',index_col=0)
        output_capacity_utilization_hours=pd.read_excel(w,sheet_name='capacity_utilization_hours',index_col=0)
        output_power_generation=pd.read_excel(w,sheet_name='power_generation',index_col=0)
        output_reneable_curtailment=pd.read_excel(w,sheet_name='reneable_curtailment',index_col=0)
        output_storages_ES_Li=pd.read_excel(w,sheet_name='storages_ES_Li',index_col=0)
        output_storages_ES_FR=pd.read_excel(w,sheet_name='storages_ES_FR',index_col=0)
        output_storages_HS=pd.read_excel(w,sheet_name='storages_HS',index_col=0)
        output_storages_AS=pd.read_excel(w,sheet_name='storages_AS',index_col=0)
        output_trade_power=pd.read_excel(w,sheet_name='trade_power',index_col=0)
        output_trans_capacity=pd.read_excel(w,sheet_name='trans_capacity',index_col=0)
        output_trans_power=pd.read_excel(w,sheet_name='trans_power',index_col=0)
        output_trans_Pipe=pd.read_excel(w,sheet_name='trans_Pipe',index_col=0)
        output_trans_Truck=pd.read_excel(w,sheet_name='trans_Truck',index_col=0)
        output_hydrogen_produce=pd.read_excel(w,sheet_name='hydrogen_produce',index_col=0)
        output_electrolyzer_on_cap=pd.read_excel(w,sheet_name='electrolyzer_on_cap',index_col=0)
        output_energy_consumption=pd.read_excel(w,sheet_name='energy_consumption',index_col=0)
        output_economics=pd.read_excel(w,sheet_name='economics',index_col=0)
        output_key_indicators=pd.read_excel(w,sheet_name='key_indicators',index_col=0)
    return output_new_capacity,output_capacity_utilization_hours,output_power_generation,output_reneable_curtailment,output_storages_ES_Li,output_storages_ES_FR,output_storages_HS,output_storages_AS,output_trade_power,output_trans_capacity,output_trans_power,output_trans_Pipe,output_trans_Truck,output_hydrogen_produce,output_electrolyzer_on_cap,output_energy_consumption,output_economics,output_key_indicators

if uploaded_model_result is not None:
    output_new_capacity,output_capacity_utilization_hours,output_power_generation,output_reneable_curtailment,output_storages_ES_Li,output_storages_ES_FR,output_storages_HS,output_storages_AS,output_trade_power,output_trans_capacity,output_trans_power,output_trans_Pipe,output_trans_Truck,output_hydrogen_produce,output_electrolyzer_on_cap,output_energy_consumption,output_economics,output_key_indicators=read_result_from_file(uploaded_model_result)

    all_available_techs=ted.all_available_techs
    available_trans_techs=ted.available_trans_techs

    get_tech_name={all_available_techs[t]:t for t in all_available_techs.keys()}
    get_trans_name={available_trans_techs[t]:t for t in available_trans_techs.keys()}

    years=[]
    nodes=[]
    arcs=[]
    for i in output_new_capacity.columns:
        if i == 'Unit':
            continue
        else:
            y=i.split('-')[0]
            n=i.split('-')[1]
            if y not in years:
                years.append(y)
            if n not in nodes:
                nodes.append(n)

    for i in output_trans_capacity.index:
        arcs.append(i)

    st.markdown('## (1)各类新建容量查询')

    st.markdown('### a.各年、各地的新建容量')

    which_new_capacity= st.selectbox(
        "选择想查询的技术",
        list(all_available_techs.keys())[:-6],
        placeholder='任选一个...',key='which_new_capacity')

    df_which_new_capacity=pd.DataFrame(0.0,index=[y for y in years],columns=[n for n in nodes]+['Unit'])
    for y in years:
        for n in nodes:
            df_which_new_capacity.loc[y,n]=output_new_capacity.loc[all_available_techs[which_new_capacity],'%s-%s'%(y,n)]
    df_which_new_capacity.loc[:,'Unit']=output_new_capacity.loc[all_available_techs[which_new_capacity],'Unit']
    st.dataframe(df_which_new_capacity)

    st.markdown('### b.各年、各线路的新建容量')

    which_new_trans= st.selectbox(
        "选择想查询的传输类型",
        available_trans_techs.keys(),
        placeholder='任选一个...',key='which_new_trans')

    df_which_new_trans=pd.DataFrame(0.0,index=[y for y in years],columns=[a for a in arcs]+['Unit'])
    for y in years:
        for a in arcs:
            df_which_new_trans.loc[y,a]=output_trans_capacity.loc[a,'%s-%s'%(y,available_trans_techs[which_new_trans])]
    df_which_new_trans.loc[:,'Unit']={'输氢-管道':r't/a','输电-电网':'MW','输氢-拖车':'t'}[which_new_trans]
    st.dataframe(df_which_new_trans)

    st.markdown('## (2)各类技术利用率查询')

    st.markdown('### a.各年、各地的利用小时数')

    which_tech_utihour= st.selectbox(
        "选择想查询的技术",
        list(all_available_techs.keys())[:-6],
        placeholder='任选一个...',key='which_tech_utihour')

    df_which_tech_utihour=pd.DataFrame(0.0,index=[y for y in years],columns=[n for n in nodes])
    for y in years:
        for n in nodes:
            df_which_tech_utihour.loc[y,n]=output_capacity_utilization_hours.loc[all_available_techs[which_tech_utihour],'%s-%s'%(y,n)]

    st.dataframe(df_which_tech_utihour)

    st.markdown('### b.发电曲线')

    which_power_techs= st.multiselect(
        "选择想读取的发电技术",
        ['发电技术-光伏', '发电技术-风电','发电技术-燃氢轮机'],
        placeholder='可选一个或多个...',key='which_power_techs')

    which_power_techs_year= st.selectbox(
        "选择想查询的年份",
        years,
        placeholder='任选一个...',key='which_power_techs_year')

    which_power_techs_node= st.selectbox(
        "选择想查询的地点",
        nodes,
        placeholder='任选一个...',key='which_power_techs_node')
    df_which_power_techs=pd.DataFrame(0.0,index=output_power_generation.index,columns=which_power_techs)
    for t in which_power_techs:
        for i in output_power_generation.index:
            df_which_power_techs.loc[i,t]=output_power_generation.loc[i,'%s-%s-%s'%(which_power_techs_year,which_power_techs_node,all_available_techs[t])]

    st.line_chart(df_which_power_techs)

    st.markdown('### c.弃电曲线')

    which_power_curt= st.multiselect(
        "选择想读取的发电技术",
        ['发电技术-光伏', '发电技术-风电'],
        placeholder='可选一个或多个...',key='which_power_curt')

    which_power_curt_year= st.selectbox(
        "选择想查询的年份",
        years,
        placeholder='任选一个...',key='which_power_curt_year')

    which_power_curt_node= st.selectbox(
        "选择想查询的地点",
        nodes,
        placeholder='任选一个...',key='which_power_curt_node')

    df_which_power_curt=pd.DataFrame(0.0,index=output_reneable_curtailment.index,columns=which_power_curt)
    for t in which_power_curt:
        df_which_power_curt.loc[:,t]=output_reneable_curtailment.loc[:,'%s-%s-%s'%(which_power_curt_year,which_power_curt_node,all_available_techs[t])]

    st.line_chart(df_which_power_curt)

    st.markdown('### d.储能设备运行曲线')

    which_storage= st.selectbox(
        "选择想读取的发电技术",
        ['储能技术-2小时锂电池', '储能技术-4小时液流电池','储氢技术-储氢罐','储氨技术-储氨罐'],
        placeholder='任选一个...',key='which_storage')

    which_storage_year= st.selectbox(
        "选择想查询的年份",
        years,
        placeholder='任选一个...',key='which_storage_year')

    which_storage_node= st.selectbox(
        "选择想查询的地点",
        nodes,
        placeholder='任选一个...',key='which_storage_node')

    which_storage_info= st.multiselect(
        "选择想查询的内容",
        ['Charge','Discharge','SOC'],default=['SOC'],
        placeholder='可选一个或多个...',key='which_storage_info')

    if len(which_storage_info)>0:
        df_which_storage=pd.DataFrame(0.0,index=output_storages_ES_Li.index,columns=which_storage_info)
        storage_df={'ES_Li':output_storages_ES_Li,'ES_FR':output_storages_ES_FR,'HS':output_storages_HS,'AS':output_storages_AS}[all_available_techs[which_storage]]
        for t in which_storage_info:
            df_which_storage.loc[:,t]=storage_df.loc[:,'%s-%s-%s'%(which_storage_year,which_storage_node,t)]

    st.line_chart(df_which_storage)

    if len(arcs) >0:
        st.markdown('### e.传输设备运行曲线')
        st.write(available_trans_techs)

        which_trans= st.selectbox(
            "选择想读取的传输类型",
            available_trans_techs.keys(),
            placeholder='任选一个...',key='which_trans')

        which_trans_year= st.selectbox(
            "选择想查询的年份",
            years,
            placeholder='任选一个...',key='which_trans_year')

        which_trans_arc= st.selectbox(
            "选择想查询的线路",
            arcs,
            placeholder='任选一个...',key='which_trans_arc')

        if available_trans_techs[which_trans] == 'Grid':
            df_which_trans=pd.DataFrame(0.0,index=output_trans_power.index,columns=['发电技术-光伏', '发电技术-风电'])
            for r in df_which_trans.columns:
                df_which_trans.loc[:,r]=output_trans_power.loc[:,'%s-%s-%s'%(which_trans_year,which_trans_arc,all_available_techs[r])]
        elif available_trans_techs[which_trans] == 'Pipe':
            df_which_trans=pd.DataFrame(0.0,index=output_trans_Pipe.index,columns=['In','Out','Volumn'])
            for r in df_which_trans.columns:
                df_which_trans.loc[:,r]=output_trans_Pipe.loc[:,'%s-%s-%s'%(which_trans_year,which_trans_arc,r)]
        elif available_trans_techs[which_trans] == 'Truck':
            df_which_trans=pd.Series(0.0,index=output_trans_Truck.index)
            df_which_trans=output_trans_Truck.loc[:,'%s-%s'%(which_trans_year,which_trans_arc)]

    st.markdown('### f.制氢技术运行曲线')

    which_hydrogen_produce= st.multiselect(
        "选择想读取的制氢技术",
        [ '电解槽技术-碱性电解槽', '电解槽技术-质子交换膜电解槽','其它制氢技术-PSA副产氢'],
        placeholder='可选一个或多个...',key='which_hydrogen_produce')

    which_hydrogen_produce_year= st.selectbox(
        "选择想查询的年份",
        years,
        placeholder='任选一个...',key='which_hydrogen_produce_year')

    which_hydrogen_produce_node= st.selectbox(
        "选择想查询的地点",
        nodes,
        placeholder='任选一个...',key='which_hydrogen_produce_node')

    df_which_hydrogen_produce=pd.DataFrame(0.0,index=output_hydrogen_produce.index,columns=which_hydrogen_produce)
    for t in which_hydrogen_produce:
        df_which_hydrogen_produce.loc[:,t]=output_hydrogen_produce.loc[:,'%s-%s-%s'%(which_hydrogen_produce_year,which_hydrogen_produce_node,all_available_techs[t])]

    st.line_chart(df_which_hydrogen_produce)

    has_electrolyzer=[]
    for t in which_hydrogen_produce:
        if all_available_techs[t] in ['AWE','PEM']:
            has_electrolyzer.append(t)
    if len(has_electrolyzer) >0:
        df_electrolyzer_on_cap=pd.DataFrame(0.0,index=output_electrolyzer_on_cap.index,columns=has_electrolyzer)

    for t in has_electrolyzer:
        df_electrolyzer_on_cap.loc[:,t]=output_electrolyzer_on_cap.loc[:,'%s-%s-%s'%(which_hydrogen_produce_year,which_hydrogen_produce_node,all_available_techs[t])]

    if has_electrolyzer:
        st.markdown('电解槽设备启动功率')
        st.line_chart(df_electrolyzer_on_cap)

    st.markdown('### g.购售电曲线')

    which_sell_power_year= st.selectbox(
        "选择想查询的年份",
        years,
        placeholder='任选一个...',key='which_sell_power_year')

    which_sell_power_node= st.selectbox(
        "选择想查询的地点",
        nodes,
        placeholder='任选一个...',key='which_sell_power_node')

    df_which_sell_power=pd.DataFrame(0.0,index=output_trade_power.index,columns=['Buy','Sell-PV','Sell-OnWIND'])

    for t in df_which_sell_power.columns:
        df_which_sell_power.loc[:,t]=output_trade_power.loc[:,'%s-%s-%s'%(which_sell_power_year,which_sell_power_node,t)]

    st.line_chart(df_which_sell_power)

    st.markdown('### h.用能曲线')

    which_energy_consumption_year= st.selectbox(
        "选择想查询的年份",
        years,
        placeholder='任选一个...',key='which_energy_consumption_year')

    which_energy_consumption_node= st.selectbox(
        "选择想查询的地点",
        nodes,
        placeholder='任选一个...',key='which_energy_consumption_node')

    which_energy_consumption= st.selectbox(
        "选择想查询的类型",
        list(all_available_techs.keys())[-6:],
        placeholder='任选一个...',key='which_energy_consumption')

    st.markdown('电力消费的单位为MWh,氢、氨消费的单位为吨。')

    df_which_energy_consumption=output_energy_consumption.loc[:,'%s-%s-%s'%(which_energy_consumption_year,which_energy_consumption_node,all_available_techs[which_energy_consumption])]

    st.line_chart(df_which_energy_consumption)

    st.markdown('## (3)经济数据')

    st.dataframe(output_economics)

    st.markdown('## (4)关键指标')

    st.dataframe(output_key_indicators)