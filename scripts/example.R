library(tidyverse)

fp <- '/Users/nickchao/Documents/codametrix/data/Healthcare Associated Infections - Hospital.csv'

hospital_df <- read_csv(fp)

hospital_df %>% 
  group_by(State, `Measure ID`) %>% 
  count() %>% 
  ggplot(aes(State, n)) +
  geom_col(aes(col = `Measure ID`))
