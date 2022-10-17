********************************************************************************
* Created 2020-02-22 by Josh Budlender (jbudlender@umass.edu)
* Last modified at least: 2022-10-17
* Last succesfully run at least: 2022-10-17

/*
  This dofile calls a Python script which downloads CPIHistory.pdf from Stats SA
  and converts the tables into two seperate CSV files, and then cleans the CSV 
  files into nice Stata format.
 
*/
********************************************************************************

* Preliminaries
clear all
set more off

cd "C:\Users\joshb\_data\HistoricSA_CPI"

local python yes

*** Python part ***

if "`python'" == "yes" {
	
	* Set python executable to my virtual environment (unless already initialized in correct location) 
	local pyenv env1
	
	python query
	if r(initialized) == 1 {
		assert "`r(execpath)'" == "C:\myprograms\Anaconda3\envs\\`pyenv'\python.exe"
	}
	else {
		python set exec "C:\myprograms\Anaconda3\envs\\`pyenv'\python.exe"
	} 
	
	* Call python script
	python script scrapeCPI.py
}




*** Stata part ***

foreach table in index rates {

	clear
	import delimited cpi_`table'.csv, varnames(1) 

	local timevars jan feb mar apr may jun jul aug sep oct nov dec

	* clean up year variable if necessary 
	cap rename v1 year
	replace year = 2009 if year ==  20092	// irritating superscript
	assert strlen(string(year)) == 4	// make sure years are all 4 digits
	export delimited using cpi_`table'.csv, replace	// save minimally cleaned version
	
	** Reshape long and nice Stata format
	
	* year average as seperate, numeric variable 
	destring average, replace dpcomma
	rename average `table'_year

	** destring and rename monthly variables to prepare for reshape
	destring `timevars', replace dpcomma
	local i = 1
	foreach var in `timevars' {
		rename `var' `table'_month`i'
		local ++i
	}

	* reshape to long 
	reshape long `table'_month, i(year) j(month)
	
	* get nice monthly date in stata format 
	gen long date_monthly = ym(year, month)
		format date_monthly %tm
	
	* clean up and save
	order year month date_monthly 
	compress 
	save cpi_`table'_long.dta, replace
	drop date_monthly
	export delimited using cpi_`table'_long.csv, replace
			
}


