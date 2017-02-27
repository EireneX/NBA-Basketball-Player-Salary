library(plm)
library(foreign)

closeAllConnections()

tmpenv <- new.env()
load("salaries_stats.RData", envir=tmpenv)
Panel <- tmpenv$panel_data_revised

library(dplyr)
grouped <- group_by(Panel, Pos)
result <- summarise(grouped, mean=mean(Salary), sd=sd(Salary), median=median(Salary))

library(gplots)
plotmeans(Salary ~ season, main="Heterogeineity across seasons", data=Panel)
plotmeans(Salary ~ Pos, main="Heterogeineity across positions", data=Panel)

library(plyr)
grouped_data <- dlply(Panel, "Pos", identity)

sink("pos_C_final.txt", append=FALSE, split=TRUE)
fixed_C <- plm(Salary ~ FGA+two_P_ptg+three_P_ptg+PF+PTS+TRB+TOV, data=grouped_data[[1]], index=c("player_id", "season"), model="within")
summary(fixed_C)
sink()

sink("pos_PF_final.txt", append=FALSE, split=TRUE)
fixed_PF <- plm(Salary ~ FGA+two_P_ptg+three_P_ptg+PF+PTS+TRB+TOV, data=grouped_data[[2]], index=c("player_id", "season"), model="within")
summary(fixed_PF)
sink()

sink("pos_PG_final.txt", append=FALSE, split=TRUE)
fixed_PG <- plm(Salary ~ FGA+two_P_ptg+three_P_ptg+PF+PTS+AST+TOV, data=grouped_data[[3]], index=c("player_id", "season"), model="within")
summary(fixed_PG)
sink()

sink("pos_SF_final.txt", append=FALSE, split=TRUE)
fixed_SF <- plm(Salary ~ FGA+two_P_ptg+three_P_ptg+PF+PTS+TOV, data=grouped_data[[4]], index=c("player_id", "season"), model="within")
summary(fixed_SF)
sink()

sink("pos_SG_final.txt", append=FALSE, split=TRUE)
fixed_SG <- plm(Salary ~ FGA+two_P_ptg+three_P_ptg+PF+PTS+TOV, data=grouped_data[[5]], index=c("player_id", "season"), model="within")
summary(fixed_SG)
sink()


random_C <- plm(Salary ~ FGA+two_P_ptg+three_P_ptg+PF+PTS+TRB+TOV, data=grouped_data[[1]], index=c("player_id", "season"), model="random")
random_PF <- plm(Salary ~ FGA+two_P_ptg+three_P_ptg+PF+PTS+TRB+TOV, data=grouped_data[[2]], index=c("player_id", "season"), model="random")
random_PG <- plm(Salary ~ FGA+two_P_ptg+three_P_ptg+PF+PTS+AST+TOV, data=grouped_data[[3]], index=c("player_id", "season"), model="random")
random_SF <- plm(Salary ~ FGA+two_P_ptg+three_P_ptg+PF+PTS+TOV, data=grouped_data[[4]], index=c("player_id", "season"), model="random")
random_SG <- plm(Salary ~ FGA+two_P_ptg+three_P_ptg+PF+PTS+TOV, data=grouped_data[[5]], index=c("player_id", "season"), model="random")

sink("hausman_tests.txt", append=FALSE, split=TRUE)
phtest(fixed_C, random_C)
phtest(fixed_PF, random_PF)
phtest(fixed_PG, random_PG)
phtest(fixed_SF, random_SF)
phtest(fixed_SG, random_SG)
sink()