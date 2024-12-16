all_available_techs={'发电技术-光伏':'PV','发电技术-风电':'OnWIND','发电技术-掺氨煤电':'COALwA','电解槽技术-碱性电解槽':'AWE','电解槽技术-质子交换膜电解槽':'PEM','储能技术-2小时锂电池':'ES_Li','储能技术-4小时液流电池':'ES_FR','储氢技术-储氢罐':'HS','其它制氢技术-变压吸附副产氢':'PSA','发电技术-燃氢轮机':'HP','发电技术-氢燃料电池':'HFC','制氨技术-空分提氮':'ASN','制氨技术-HB氨合成':'HBA','储氨技术-储氨罐':'AS','制甲醇技术-合成器':'MSR','储醇技术-储醇罐':'MS','电力用户-小时固定用户':'PD-hourfix','电力用户-日内可调节用户':'PD-dayfix','氢用户-小时固定用户':'HD-hourfix','氢用户-日内可调节用户':'HD-dayfix','氨用户-小时固定用户':'AD-hourfix','氨用户-日内可调节用户':'AD-dayfix','甲醇用户-小时固定用户':'MD-hourfix','甲醇用户-日内可调节用户':'MD-dayfix'}

consume_type_amount=8

available_trans_techs={'输电-电网':'Grid','输氢-管道':'Pipe','输氢-拖车':'Truck'}

def read_techecon_data(periods_year):
    techecon_data={t:{'type':'undef','unit':{'cap':0.0,'cap_unit':'undef','life':0.0,'fixed_cost':{y:0.0 for y in periods_year},'fixed_cost_unit':'undef','OMC_rate':0.0},'coef':{}} for t in list(all_available_techs.values())[:-consume_type_amount]+list(available_trans_techs.values())}

    techecon_data['PV']['type']='Power_generation'
    techecon_data['PV']['unit']['cap']=0.01
    techecon_data['PV']['unit']['cap_unit']='MW'
    for y in periods_year:
        techecon_data['PV']['unit']['fixed_cost'][y]=30
    techecon_data['PV']['unit']['fixed_cost_unit']='kRMB'
    techecon_data['PV']['unit']['life']=25
    techecon_data['PV']['unit']['OMC_rate']=0.015

    techecon_data['OnWIND']['type']='Power_generation'
    techecon_data['OnWIND']['unit']['cap']=0.05
    techecon_data['OnWIND']['unit']['cap_unit']='MW'
    for y in periods_year:
        techecon_data['OnWIND']['unit']['fixed_cost'][y]=225
    techecon_data['OnWIND']['unit']['fixed_cost_unit']='kRMB'
    techecon_data['OnWIND']['unit']['life']=20
    techecon_data['OnWIND']['unit']['OMC_rate']=0.015

    techecon_data['COALwA']['type']='Power_generation'
    techecon_data['COALwA']['unit']['cap']=300
    techecon_data['COALwA']['unit']['cap_unit']='MW'
    for y in periods_year:
        techecon_data['COALwA']['unit']['fixed_cost'][y]=4*300*1000
    techecon_data['COALwA']['unit']['fixed_cost_unit']='kRMB'
    techecon_data['COALwA']['unit']['life']=40
    techecon_data['COALwA']['unit']['OMC_rate']=0.015
    techecon_data['COALwA']['coef']['Ramp_rate']=0.2
    techecon_data['COALwA']['coef']['coal_consumption_t_per_MWh']=0.3
    techecon_data['COALwA']['coef']['coal_price_kRMB_per_t']=1.0
    techecon_data['COALwA']['coef']['co2_emission_t_per_t']=2.64
    techecon_data['COALwA']['coef']['ammonia_consumption_t_per_MWh']=0.4

    techecon_data['ES_Li']['type']='Storage'
    techecon_data['ES_Li']['unit']['cap']=0.005
    techecon_data['ES_Li']['unit']['cap_unit']='MW'
    techecon_data['ES_Li']['coef']['Capacity_to_rate']=2
    for y in periods_year:
        techecon_data['ES_Li']['unit']['fixed_cost'][y]=techecon_data['ES_Li']['unit']['cap']*techecon_data['ES_Li']['coef']['Capacity_to_rate']*1000.0
    techecon_data['ES_Li']['unit']['fixed_cost_unit']='kRMB'
    techecon_data['ES_Li']['unit']['life']=6
    techecon_data['ES_Li']['unit']['OMC_rate']=0.005
    techecon_data['ES_Li']['coef']['mini_soc_rate_of_capacity']=0.1
    techecon_data['ES_Li']['coef']['Charge_efficient']=0.95
    techecon_data['ES_Li']['coef']['Discharge_efficient']=0.95

    techecon_data['ES_FR']['type']='Storage'
    techecon_data['ES_FR']['unit']['cap']=0.5
    techecon_data['ES_FR']['unit']['cap_unit']='MW'
    techecon_data['ES_FR']['coef']['Capacity_to_rate']=4
    for y in periods_year:
        techecon_data['ES_FR']['unit']['fixed_cost'][y]=techecon_data['ES_FR']['unit']['cap']*techecon_data['ES_FR']['coef']['Capacity_to_rate']*375.0+techecon_data['ES_FR']['unit']['cap']*400.0
    techecon_data['ES_FR']['unit']['fixed_cost_unit']='kRMB'
    techecon_data['ES_FR']['unit']['life']=20
    techecon_data['ES_FR']['unit']['OMC_rate']=0.005
    techecon_data['ES_FR']['coef']['Charge_efficient']=0.8
    techecon_data['ES_FR']['coef']['mini_soc_rate_of_capacity']=0.1
    techecon_data['ES_FR']['coef']['Discharge_efficient']=0.8

    techecon_data['Grid']['type']='Trans'
    techecon_data['Grid']['unit']['cap']=100
    techecon_data['Grid']['unit']['cap_unit']='MW'
    for y in periods_year:
        techecon_data['Grid']['unit']['fixed_cost'][y]=1200
    techecon_data['Grid']['unit']['fixed_cost_unit']='kRMB/km'
    techecon_data['Grid']['unit']['life']=60
    techecon_data['Grid']['unit']['OMC_rate']=0.01
    techecon_data['Grid']['coef']['Transformer_cost_per_line_kRMB']=28000.0*2

    techecon_data['AWE']['type']='Hydrogen_producer'
    techecon_data['AWE']['unit']['cap']=5
    techecon_data['AWE']['unit']['cap_unit']='MW'
    for y in periods_year:
        techecon_data['AWE']['unit']['fixed_cost'][y]=5000
    techecon_data['AWE']['unit']['fixed_cost_unit']='kRMB'
    techecon_data['AWE']['unit']['life']=10
    techecon_data['AWE']['unit']['OMC_rate']=0.02
    techecon_data['AWE']['coef']['power_MWh_per_hydrogen_t']={}
    for y in periods_year:
        techecon_data['AWE']['coef']['power_MWh_per_hydrogen_t'][y]=56
    techecon_data['AWE']['coef']['mini_opration_rate']={}
    for y in periods_year:
        techecon_data['AWE']['coef']['mini_opration_rate'][y]=0.3
    techecon_data['AWE']['coef']['water_t_per_hydrogen_t']=30
    techecon_data['AWE']['coef']['water_price_kRMB_per_t']=0.007

    techecon_data['PEM']['type']='Hydrogen_producer'
    techecon_data['PEM']['unit']['cap']=5
    techecon_data['PEM']['unit']['cap_unit']='MW'
    for y in periods_year:
        techecon_data['PEM']['unit']['fixed_cost'][y]=8000
    techecon_data['PEM']['unit']['fixed_cost_unit']='kRMB'
    techecon_data['PEM']['unit']['life']=10
    techecon_data['PEM']['unit']['OMC_rate']=0.02
    techecon_data['PEM']['coef']['power_MWh_per_hydrogen_t']={}
    for y in periods_year:
        techecon_data['PEM']['coef']['power_MWh_per_hydrogen_t'][y]=56
    techecon_data['PEM']['coef']['mini_opration_rate']={}
    for y in periods_year:
        techecon_data['PEM']['coef']['mini_opration_rate'][y]=0.05
    techecon_data['PEM']['coef']['water_t_per_hydrogen_t']=30
    techecon_data['PEM']['coef']['water_price_kRMB_per_t']=0.007

    techecon_data['PSA']['type']='Hydrogen_producer'
    techecon_data['PSA']['unit']['cap']=0.1
    techecon_data['PSA']['unit']['cap_unit']='t/hour'
    for y in periods_year:
        techecon_data['PSA']['unit']['fixed_cost'][y]=600
    techecon_data['PSA']['unit']['fixed_cost_unit']='kRMB'
    techecon_data['PSA']['unit']['life']=10
    techecon_data['PSA']['unit']['OMC_rate']=0.5/6
    techecon_data['PSA']['coef']['variable_cost_kRMB_per_t']=20.16
    techecon_data['PSA']['coef']['hourly_curve']={h:1.0 for h in range(8760)}

    ## TODO:data of ammonia needs calibration
    techecon_data['ASN']['type']='Ammonia_producer'
    techecon_data['ASN']['unit']['cap']=0.1
    techecon_data['ASN']['unit']['cap_unit']='t/hour'
    for y in periods_year:
        techecon_data['ASN']['unit']['fixed_cost'][y]=2.835
    techecon_data['ASN']['unit']['fixed_cost_unit']='kRMB'
    techecon_data['ASN']['unit']['life']=10
    techecon_data['ASN']['unit']['OMC_rate']=0.72/2.835
    techecon_data['ASN']['coef']['power_MWh_per_N2_t']=1.25

    techecon_data['HBA']['type']='Ammonia_producer'
    techecon_data['HBA']['unit']['cap']=0.1
    techecon_data['HBA']['unit']['cap_unit']='t/hour'
    for y in periods_year:
        techecon_data['HBA']['unit']['fixed_cost'][y]=34.49
    techecon_data['HBA']['unit']['fixed_cost_unit']='kRMB'
    techecon_data['HBA']['unit']['life']=10
    techecon_data['HBA']['unit']['OMC_rate']=0.11/344.9
    techecon_data['HBA']['coef']['power_MWh_per_NH3_t']=1/3.1
    techecon_data['HBA']['coef']['H2_t_per_NH3_t']=3.0/17.0
    techecon_data['HBA']['coef']['N2_t_per_NH3_t']=14.0/17.0

    ## TODO:data of methanol needs calibration
    techecon_data['MSR']['type']='Methanol_producer'
    techecon_data['MSR']['unit']['cap']=0.1
    techecon_data['MSR']['unit']['cap_unit']='t/hour'
    for y in periods_year:
        techecon_data['MSR']['unit']['fixed_cost'][y]=2.835
    techecon_data['MSR']['unit']['fixed_cost_unit']='kRMB'
    techecon_data['MSR']['unit']['life']=10
    techecon_data['MSR']['unit']['OMC_rate']=0.72/2.835
    techecon_data['MSR']['coef']['power_MWh_per_CH3OH_t']=1.25
    techecon_data['MSR']['coef']['H2_t_per_CH3OH_t']=0.194
    techecon_data['MSR']['coef']['CO2_t_per_CH3OH_t']=1.44
    techecon_data['MSR']['coef']['CO2_price_kRMB_per_t']=0.2

    techecon_data['MS']['type']='Storage'
    techecon_data['MS']['unit']['cap']=1
    techecon_data['MS']['unit']['cap_unit']='t/hour'
    techecon_data['MS']['coef']['Capacity_to_rate']=1
    for y in periods_year:
        techecon_data['MS']['unit']['fixed_cost'][y]=0.57
    techecon_data['MS']['unit']['fixed_cost_unit']='kRMB'
    techecon_data['MS']['unit']['life']=50
    techecon_data['MS']['unit']['OMC_rate']=0.01
    techecon_data['MS']['coef']['mini_soc_rate_of_capacity']=0.05
    techecon_data['MS']['coef']['Charge_efficient']=0.999
    techecon_data['MS']['coef']['Discharge_efficient']=0.999

    techecon_data['AS']['type']='Storage'
    techecon_data['AS']['unit']['cap']=1
    techecon_data['AS']['unit']['cap_unit']='t/hour'
    techecon_data['AS']['coef']['Capacity_to_rate']=1
    for y in periods_year:
        techecon_data['AS']['unit']['fixed_cost'][y]=0.57
    techecon_data['AS']['unit']['fixed_cost_unit']='kRMB'
    techecon_data['AS']['unit']['life']=50
    techecon_data['AS']['unit']['OMC_rate']=0.01
    techecon_data['AS']['coef']['mini_soc_rate_of_capacity']=0.05
    techecon_data['AS']['coef']['Charge_efficient']=0.999
    techecon_data['AS']['coef']['Discharge_efficient']=0.999

    techecon_data['HS']['type']='Storage'
    techecon_data['HS']['unit']['cap']=1
    techecon_data['HS']['unit']['cap_unit']='t/hour'
    techecon_data['HS']['coef']['Capacity_to_rate']=5
    for y in periods_year:
        techecon_data['HS']['unit']['fixed_cost'][y]=150000.0
    techecon_data['HS']['unit']['fixed_cost_unit']='kRMB'
    techecon_data['HS']['unit']['life']=60
    techecon_data['HS']['unit']['OMC_rate']=0.01
    techecon_data['HS']['coef']['mini_soc_rate_of_capacity']=0.02
    techecon_data['HS']['coef']['Charge_efficient']=0.99999
    techecon_data['HS']['coef']['Discharge_efficient']=0.99999

    techecon_data['Pipe']['type']='Trans'
    techecon_data['Pipe']['unit']['cap']=100000
    techecon_data['Pipe']['unit']['cap_unit']='t/a'
    techecon_data['Pipe']['coef']['radius_meter']=0.500/2
    techecon_data['Pipe']['coef']['pressure_vary_rates_of_standard']=0.05
    techecon_data['Pipe']['coef']['standard_pressure_MPa']=3.5
    for y in periods_year:
        techecon_data['Pipe']['unit']['fixed_cost'][y]=5800
    techecon_data['Pipe']['unit']['fixed_cost_unit']='kRMB/km'
    techecon_data['Pipe']['unit']['life']=60
    techecon_data['Pipe']['unit']['OMC_rate']=0.01
    techecon_data['Pipe']['coef']['inout_variable_cost_kRMB_per_t']=0.5
    techecon_data['Pipe']['coef']['Max_in']=14
    techecon_data['Pipe']['coef']['Max_out']=8
    techecon_data['Pipe']['coef']['Cycle_eff']=0.9999

    techecon_data['Truck']['type']='Trans'
    techecon_data['Truck']['unit']['cap']=0.63
    techecon_data['Truck']['unit']['cap_unit']='t_per_vehicle'
    for y in periods_year:
        techecon_data['Truck']['unit']['fixed_cost'][y]=1200
    techecon_data['Truck']['unit']['fixed_cost_unit']='kRMB'
    techecon_data['Truck']['unit']['life']=20
    techecon_data['Truck']['unit']['OMC_rate']=0.03
    techecon_data['Truck']['coef']['running_speed_km_per_h']=60
    techecon_data['Truck']['coef']['variable_cost_kRMB_per_tkm']=0.01
    techecon_data['Truck']['coef']['Cycle_eff']=0.9999

    techecon_data['HP']['type']='Power_generation'
    techecon_data['HP']['unit']['cap']=0.5
    techecon_data['HP']['unit']['cap_unit']='MW'
    for y in periods_year:
        techecon_data['HP']['unit']['fixed_cost'][y]=1500
    techecon_data['HP']['unit']['fixed_cost_unit']='kRMB'
    techecon_data['HP']['unit']['life']=30
    techecon_data['HP']['unit']['OMC_rate']=0.03
    techecon_data['HP']['coef']['hydrogen_to_power_t_per_MWh']=1/15.0

    techecon_data['HFC']['type']='Power_generation'
    techecon_data['HFC']['unit']['cap']=0.11
    techecon_data['HFC']['unit']['cap_unit']='MW'
    for y in periods_year:
        techecon_data['HFC']['unit']['fixed_cost'][y]=3429
    techecon_data['HFC']['unit']['fixed_cost_unit']='kRMB'
    techecon_data['HFC']['unit']['life']=10
    techecon_data['HFC']['unit']['OMC_rate']=0.03
    techecon_data['HFC']['coef']['hydrogen_to_power_t_per_MWh']=1/15.0
    return techecon_data