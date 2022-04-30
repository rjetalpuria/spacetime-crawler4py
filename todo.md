# TODO List for the Project:  
- [x] check if the url has one of the following domails:
	*.ics.uci.edu/*  
	*.cs.uci.edu/*  
	*.informatics.uci.edu/*  
	*.stat.uci.edu/*  
	today.uci.edu/department/information_computer_sciences/*
  
- [x] gather info for project report:  
	number of unique pages  
	longest page   
	50 most common words   
	list of subdomains under ics.uci.edu   
  
- [x] scrapper:
	make sure the urls are within domins  
	make sure to defragment the urls  
  
- [x] watchout for traps  
  
- [x] crawler behavior:  
	honor the politeness delay  
	crawl all pages with high textual information content  
	detect and avoid infinite traps  
	detect and avoid sets of similar pages with no information  
	detect and avoid dead urls that return 200 status but no data  
	detect and avoid crawling very large files, especially if they have low information value  
  
- [x] transform relative URLs to absolute URLs  
- [x] add comments   
- [x] make sure you are sending server a request with an ASCII url and neither the HTML content of the webpage nor UNICODE strings   
- [x] simple automatic trap detection based on URL patterns and/or content similarity repetition over certain amount of chained pages    
