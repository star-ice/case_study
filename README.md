# case_study

<p>case_study_result stores all figures and text results.</p>
<p>After opening .html files in browser, figures can be downlowded with .png format from the webpage.</p>

<p>data contains all case information which was stored as csv file and can be viewed in excel.</p>

<p>to_be_checked contains files that need to be corrected by Profs.</p>

+ Code Interpretation
 	+ case_proces
 		+ process_details
			+ case_process_improved
			      + process raw json file--->structural json file, generate  case dict files
			      + Phrase Matcher, entity recognition class, entity ruler, tokenizer, spacy pipeline
			      + token2vec
			+ common_build_csv_pd
				+ generate all_cases.csv from csv_graph
				+ adding plaintiff, defendant, lawyer information for each case
			+ case_to_graph_only_method
				+ generate csv_graph from csv files in total_dict_result/modified.csv, which contains information from all case dict files
			+ case_to_pd
				+ generate modified.csv from all case dict files
    		+ basic_information
     			+ case_to_graph_basic_information
      				+ descriptive information of cases(1st, 2nd), plaintiffs, defendants, procedures, penalty, object money, (and legal fee)
     			+ MoransI
      				+ explore whether case amount is relevant to provinces
     			+ caseNeo4j
      				+ generate data for neo4j use
    		+ plaintiffs
     			+ activePlaintiffPatterns1
      				+ descriptive information about the first 200 active plaintiffs and their cases
      				+ Still have problems to be solved
       					+ 用neo4j分析活跃原告和其被告的关系，可以分析重要的活跃原告，重要的被告，以及原告-被告pair
       					+ 用分类问题的方法解决是否活跃原告在赢率，案件数都比较高的地区出现（省级和市级都做一下）
     			+ activePlaintiffPatterns2
      				+ analytical information about the first 200 active plaintiffs and their cases
     			+ activePlaintiffPatterns3
      				+ analyse the reason why active plaintiffs exit
     			+ activePlaintiffPatterns4
      				+ community analysis about 200 active plaintiffs
     			+ plaintiffLawyerCommunityVisual
      				+ Visualise community with sigma.js
      				+ G_3_2.gexf contains community of plaintiffs that cooperated with the same lawyer
     			+ plaintiffCommunityAnalysis
      				+ Prove the validity of community in graph G_3 in active_plaintiff_patterns4
      				+ Analyse lawyers of communities
