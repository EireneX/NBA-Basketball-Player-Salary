install.packages("sqldf")

library(sqldf) 

#Dataset details
data<-read.csv("stats.csv",header=TRUE,sep=",")

data <- data[complete.cases(data),]

tablePG <- sqldf("SELECT * FROM data WHERE Pos = 'PG' ")
tableSG <- sqldf("SELECT * FROM data WHERE Pos = 'SG' ")
tableSF <- sqldf("SELECT * FROM data WHERE Pos = 'SF' ")
tablePF <- sqldf("SELECT * FROM data WHERE Pos = 'PF' ")
tableC <- sqldf("SELECT * FROM data WHERE Pos = 'C' ")

regPG <-lm(Salary ~ log(G)  + MP + X3P + X3P. + AST + STL + PTS , data=tablePG)
summary(regPG)
summary(regPG)$r.square      # r square
summary(regPG)$adj.r.square  # adjusted r square
print(regPG)
par(mfrow=c(2,2))
plot(regPG)
pairs(tablePG[,c(29,5,23,25,28)],panel = panel.smooth, cex=0.25, main="Variables analysis for PG")

regSG <-lm(Salary ~ log(G) + MP + X3P + X3P. + AST + BLK + PTS , data=tablePG)
summary(regSG)
summary(regSG)$r.square      # r square
summary(regSG)$adj.r.square  # adjusted r square
print(regSG)
par(mfrow=c(2,2))
plot(regPG)

regSF <-lm(Salary ~ log(G) + MP + FG + FG. + STL + PTS + BLK, data=tablePF)
summary(regSF)
summary(regSF)$r.square      # r square
summary(regSF)$adj.r.square  # adjusted r square
print(regSF)
par(mfrow=c(2,2))
plot(regSF)

regPF <-lm(Salary ~ G + MP + FG + X2P + FT + PTS + BLK, data=tablePF)
summary(regPF)
summary(regPF)$r.square      # r square
summary(regPF)$adj.r.square  # adjusted r square
print(regPF)
par(mfrow=c(2,2))
plot(regPF)

regC <-lm(Salary ~ G + MP + X2P + FT + TRB + PTS, data=tableC)
summary(regC)
summary(regC)$r.square      # r square
summary(regC)$adj.r.square  # adjusted r square
print(regC)
par(mfrow=c(2,2))
plot(regC)
