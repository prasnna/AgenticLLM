from nltk.corpus import wordnet

def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return synonyms

def generate_real_world_tokens(sql_query):
    tokens = sql_query.split()
    real_world_tokens = []
    for token in tokens:
        synonyms = get_synonyms(token)
        if synonyms:
            real_world_tokens.extend(synonyms)
        else:
            real_world_tokens.append(token)
    return real_world_tokens

# Example SQL query
sql_query = "SELECT DISTINCT TAH3.LEVEL_CODE AS BRANCH_CODE, tah2.level_code AS AGENCY_CODE, CASE WHEN tb1.first_name != '' OR tb.first_name != NULL THEN Rtrim(tb1.first_name) + ' ' + Rtrim(tb1.last_name) ELSE tb1.company_name END AS AGENCY_NAME, tah1.level_code AS PRODUCER_CODE, CASE WHEN tb.first_name != '' OR tb.first_name != NULL THEN Rtrim(tb.first_name) + ' ' + Rtrim(tb.last_name) ELSE tb.company_name END AS PRODUCER_NAME, tc.CONTRACT_ID, tcorp.co_corp_code AS COMPANY, tc.state AS CONTRACT_STATE, tc.LOB, tc.CONTRACT_TYPE, tc.CONTRACT_STATUS, tc.CONTRACT_EFF_DATE, tc.NEW_BUS_IND, tc.[WEB_DISPLAY_NAME], [POLICY_SYSTEM_CONFIGURED], [CONTRACT_NUMBER], [DATE_COMPANY_SIGNED], [NEW_BUS_IND], [MVR_CLUE], [AGENCY_APPOINTMENT_DATE], [CONTRACT_TYPE], [CONTRACT_STATUS], [CONTRACT_EFF_DATE], [CONTRACT_EXP_DATE], [NB_TERM_DATE], [RENEWAL_TERM_DATE], [BINDING_AUTHORITY], [TIP], [GROUP_ID], [GROUP_CHARITABLE], [PAYROLL_DEDUCT], [BOOK_TRANSFER_SOURCE], [BOOK_TRANSFER_PREMIUM], [AGENCY_SYSTEM_DISPLAY_IND], [SERVICE_CENTER_IND], [SERVICE_CENTER_PCT_FEE], [ESALES_ELIGIBLITY_CODE], [PRFT_SHARING_RLP_CODE], [CLUSTER_NAME], [PROFIT_SHARING], [SECOND_RT_AGENCY_GRP], [SUPER_AGENT_IND], [COMP_RATER_IND], [RC1_DFLT], CASE WHEN tb3.COMPANY_NAME != '' THEN (Rtrim(tb3.company_name) + '(Group Id:' + CONVERT(VARCHAR(20), trg.rollup_group_id) + ')') ELSE (Rtrim(tb3.first_name) + ' ' + Rtrim(tb3.last_name) + '(Group Id:' + CONVERT(VARCHAR(20), trg.rollup_group_id) + ')') END AS COMMISSION_GROUP, TRC.ORG_GROUP_NAME, TRC.ORG_CHANNEL_NAME, TRC.ORG_SUB_CHANNEL_NAME, [FIRST_PRIOR_AGENCY_NAME], [SECOND_PRIOR_AGENCY_NAME], [AQM_FLAG], [AI_DISPLAY], [REPORTING_HIERARCHY], [PERFORMANCE_IMPROVEMENT_PLAN], [PERFORMANCE_IMPROVEMENT_PLAN_DATE], [PERFORMANCE_IMPROVEMENT_PLAN_GRADUATION_DATE], ts.LIST_VALUE as UW_GRP FROM tbl_contract tc WITH(nolock) JOIN tbl_agent_hierarchy tah1 WITH(nolock) ON tah1.agent_hier_id = tc.agent_hier_id AND tah1.level = '002' AND tc.STATE in ('CT', 'NH') and tc.LOB = 'Homeowners' JOIN tbl_agent_hierarchy tah2 WITH(nolock) ON tah1.parent_hier_id = tah2.agent_hier_id AND tah2.DELETE_STATUS != 'D' JOIN TBL_AGENT_HIERARCHY tah3 with(nolock) ON tah2.PARENT_HIER_ID=tah3.AGENT_HIER_ID AND tah3.DELETE_STATUS != 'D' JOIN tbl_company_corporation_hierarchy tcorp WITH(nolock) ON tcorp.co_corp_id = tc.co_corp_id and tcorp.CO_CORP_CODE like 'ALN_%' JOIN tbl_business_entity_agent_hier_relationship tr WITH(nolock) ON tah1.agent_hier_id = tr.agent_hier_id JOIN tbl_business_entity tb WITH(nolock) ON tr.bus_entity_id = tb.bus_entity_id JOIN tbl_business_entity_agent_hier_relationship tr1 WITH(nolock) ON tah2.agent_hier_id = tr1.agent_hier_id JOIN tbl_business_entity tb1 WITH(nolock) ON tr1.bus_entity_id = tb1.bus_entity_id left outer JOIN TBL_ROLLUP_GROUP_MEMBERSHIP TRGM ON tc.CONTRACT_ID=TRGM.CONTRACT_ID left outer JOIN TBL_ROLLUP_GROUP TRG ON TRGM.ROLLUP_GROUP_ID=TRG.ROLLUP_GROUP_ID left outer join TBL_AGENT_HIERARCHY tah4 WITH(nolock) ON TRG.AGENT_HIER_ID = tah4.AGENT_HIER_ID left outer JOIN tbl_business_entity_agent_hier_relationship tr3 WITH(nolock) ON tah4.agent_hier_id = tr3.agent_hier_id left outer JOIN tbl_business_entity tb3 WITH(nolock) ON tr3.bus_entity_id = tb3.bus_entity_id left outer JOIN TBL_RPTG_CHANNEL_INFO TRC WITH(NOLOCK) ON TRC.CONTRACT_ID=tc.CONTRACT_ID left outer JOIN TBL_RPTG_CONTRACT_INFO TRCI WITH(NOLOCK) ON TRCI.CONTRACT_ID=tc.CONTRACT_ID left outer JOIN TBL_LIST_VALUE_CONTRACT_XREF TL WITH(NOLOCK) ON tc.CONTRACT_ID= TL.CONTRACT_ID join TBL_SUPP_DISPLAY_TYPE ts with(nolock) on TL.DISPLAY_TYPE_ID=ts.DISPLAY_TYPE_ID And ts.LIST_NAME='UW_GRP' order by tah2.LEVEL_CODE"

# Generate real-world tokens
real_world_tokens = generate_real_world_tokens(sql_query)
print(real_world_tokens)
