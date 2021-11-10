# case_study

### Workflow

![alt text](https://github.com/star-ice/case_study/blob/main/materials/project_steps.jpeg?raw=true)

### Supplementary Description

+ Directory *case_study_result* stores all figures, networks and text results.

+ After opening .html files in browser, figures can be downlowded with .png format from the webpage.

+ Directory *data* contains all case information which was stored as csv file and can be viewed in excel.

+ Directory *to_be_checked* contains files that need to be corrected by Profs.

### Code Interpretation
+ case_process
	+ process_details
		+ case_process_improved
			+ Process raw json file to structural json file, generate case dict files
			+ Phrase Matcher, entity recognition class, entity ruler, tokenizer, spacy pipeline
			+ Token2vec
		+ common_build_csv_pd
			+ Generate all_cases.csv from csv_graph
			+ Adding plaintiff, defendant, lawyer information for each case
		+ case_to_graph_only_method
			+ Generate csv_graph from csv files in total_dict_result/modified.csv, which contains information from all case dict files
		+ case_to_pd
			+ Generate modified.csv from all case dict files
	+ basic_information
		+ case_to_graph_basic_information
			+ Descriptive information of cases(1st, 2nd), plaintiffs, defendants, procedures, penalty, object money, (and legal fee)
		+  MoransI
			+  Explore whether case amount is relevant to provinces
		+  caseNeo4j
			+  Generate data for neo4j use
	+  plaintiffs
		+  activePlaintiffPatterns1
			+  Descriptive information about the first 200 active plaintiffs and their cases
			+  Still have problems to be solved
				+  用neo4j分析活跃原告和其被告的关系，可以分析重要的活跃原告，重要的被告，以及原告-被告pair
		+  activePlaintiffPatterns2
			+  Analytical information about the first 200 active plaintiffs and their cases
		+  activePlaintiffPatterns3
			+  Analyse the reason why active plaintiffs exit
		+  activePlaintiffPatterns4
			+  community analysis about 200 active plaintiffs
		+  plaintiffLawyerCommunityVisual
			+  Visualise community with sigma.js
			+  G_3_2.gexf contains community of plaintiffs that cooperated with the same lawyer
		+  plaintiffCommunityAnalysis
			+  Prove the validity of community in graph G_3 in active_plaintiff_patterns4
			+  Analyse lawyers of communities
		+  plaintiffLawyer
			+  Descriptive and analytical information about cases with lawyers and were sued by the first 200 active plaintiffs 
+ reasonExtract
	+ caseReasonExtract
		+ extract case reasons through reason keywords match, and then vote match times to find the primary reason
	+  LDA
		+  Find case reason categories and keywords in each category from "court held" contents
	+  resultDisplay
		+  Descriptive information for case reasons
	+  textcnn
		+  classify "court held" content into specific case reason with self-defined reason category
+  case_crawler
	+  Lawsdata website crawler based on python Scrapy frame
