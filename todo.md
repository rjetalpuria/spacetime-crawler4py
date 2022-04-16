# TODO List for the Project:
- [x] check if the url has one of the following domails: ---Rushi
	*.ics.uci.edu/*
	*.cs.uci.edu/*
	*.informatics.uci.edu/*
	*.stat.uci.edu/*
	today.uci.edu/department/information_computer_sciences/* ----Rushi: not sure about this one

- [ ] gather info for project report:
	number of unique pages
	longest page 
	50 most common words 
	list of subdomains under ics.uci.edu

- [x] scrapper: ---Rushi
	make sure the urls are within domins
	make sure to defragment the urls

- [ ] watchout for traps

- [ ] crawler behavior:
	honor the politeness delay
	crawl all pages with high textual information content
	detect and avoid infinite traps
	detect and avoid sets of similar pages with no information
	detect and avoid dead urls that return 200 status but no data
	detect and avoid crawling very large files, especially if they have low information value

- [ ] transform relative URLs to absolute URLs
- [ ] add comments 
- [ ] make sure you are sending server a request with an ASCII url and neither the HTML content of the webpage nor UNICODE strings
- [ ] simple automatic trap detection based on URL patterns and/or content similarity repetition over certain amount of chained pages 
