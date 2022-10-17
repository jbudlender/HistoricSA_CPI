## Machine-readable South African CPI history

Stats SA provides a monthly headline CPI series back to 1980 and year-on-year inflation rates to 1911, but the series are trapped in a pdf.

The short Stata do file `readCPI_master.do` fetches and extracts the series by calling the Python script `scrapeCPI.py` and then cleans the data and reshapes into long format.

I provide Stata .dta files and CSVs.
