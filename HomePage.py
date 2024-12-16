import streamlit as st

st.set_page_config(
    page_title="绿氢系统运行规划决策分析平台",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "正在建设…"
    }
)

#st.title('维护更新中，请勿使用！')

st.title('绿氢系统运行规划决策分析平台 V0.62 Beta')

st.markdown('## 使用说明')
st.markdown('通过模型设置页面生成模型输入json文件,该文件在运行模型页面导入后可以运行模型并生成模型结果Excel文件,模型结果文件可以直接读取或通过读取结果页面上传后进行结果可视化。')

st.markdown('## 版本更新')
st.markdown('### V0.62 Beta 2024/11/28')
st.markdown('优化了模型设置逻辑.')

st.markdown('### V0.61 Beta 2024/11/25')
st.markdown('可以按省-市分级选择.')

st.markdown('### V0.6 Beta 2024/11/20')
st.markdown('增加了煤电掺氨, 还不太可用, 有待调试.')

st.markdown('### V0.5 Beta 2024/11/4')
st.markdown('增加了多区域功能,即将不同的节点设置为不同的地区.理论上支持了全国多区域规划.模型规模以及可求解性还需要进一步测试.已有功能不受影响.')

st.markdown('### V0.4 2024/10/24')
st.markdown('增加了甲醇系统; 具体包括: (1)甲醇需求,形式同电氢氨;(2)需要输入一个外生甲醇价; (3)增加了两个技术:合成甲醇的设备甲醇合成器MSR,储甲醇罐MS,有甲醇需求的节点MSR必选.')

st.markdown('### V0.32 2024/10/24')
st.markdown('(1)增加了燃料电池; (2)修复了一些bug.')

st.markdown('### V0.31 2024/09/27')
st.markdown('(1)输出excel增加了当前地点的风光容量因子曲线; (2)重新计算了各地的风格容量因子; (3)修复了一些bug.')


st.markdown('### V0.3 2024/09/22')
st.markdown('(1)在模型设置页面增加了各类技术的参数修改; (2)在模型中增加了一种电量交换模式,可以选择年度互换平衡,也可以月度平衡.')

st.markdown('### V0.2 2024/09/19')
st.markdown('增加了氨系统. 具体包括: (1)氨需求,跟电氢一样; (2)需要输入一个外生氨价; (3)增加了三个技术:制氮气需要的空气分离设备ASN,合成氨的设备HBA,储氨罐AS,有氨需求的节点前两个必选.')

st.markdown('### V0.1 2024/08/19')
st.markdown('上线测试.已完成电,氢两个系统.')

st.sidebar.markdown("@Copyright 华北电力大学 王歌课题组")
st.sidebar.markdown("欢迎提出意见和建议!")
st.sidebar.markdown("E-mail: wangge@ncepu.edu.cn")