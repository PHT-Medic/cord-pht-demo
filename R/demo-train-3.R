############################################################################################################################
##         Zur Alterspyramide zu rechnen
##############################################################################################################################
library(tidyverse)
library(eeptools) # um Alter zu berechnen
library(ggplot2)# fC<r muster age pyramid
library(fhircrackr)

# empty global enviroment
rm(list = ls())

# ignore warnings
options(warn=-1)

# load Data from imported FHIR
loaded_bundles <- fhir_load("/opt/train_data/")
design <- list(
  Condition = list(
    resource = "//Condition",
    cols = list(
      clinical_status = "clinicalStatus/coding/code",
      icd_10 = "code/coding/code",
      icd_10_des = "code/coding/display",
      pat_ref = "subject/reference",
      date = "meta/lastUpdated"
    )
  )
)

# crack fhir bundles
dfs <- fhir_crack(loaded_bundles, design)

# save raw patients dataframe
data <- dfs$Condition

result  <- as.data.frame(data %>%
                         group_by(  icd_10) %>%
                          summarise(Anzahl = n()))

# Barplot
ggplot(result, aes(x=icd_10, y=Anzahl)) + 
  geom_bar(stat = "identity")

#Data folder for results
result_folder <- "./opt/pht_results/"

# save image to file
ggsave(paste0(result_folder,"result_graph_conditions.png"))

# Check if previous result exists and add it up to our current ersult
if (file.exists(paste(result_folder,"result_condition.csv", sep = ""))) {
  #read previous results
  previous_result <- read.csv2(paste0(result_folder,"result_condition.csv"))
  
  #add up result with found results
  result <- result %>% bind_rows(
    previous_result
  ) %>% 
    group_by(icd_10) %>% 
    dplyr::summarize(Anzahl = sum(Anzahl))

  message("previous PHT result found -> Add up")
}

#write result to file for next station
write.csv2(result, paste0(result_folder,"result_condition.csv"), row.names = FALSE)

