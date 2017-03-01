library(ggplot2)
stats <- read.csv("~/Desktop/avgdata.csv",header=TRUE,sep=",")

# Remove rows with NA data
data <- stats[complete.cases(stats),]
#Data for different position
PGdata <- data[data$Pos=="PG",]
Cdata <- data[data$Pos=="C",]
PFdata <- data[data$Pos=="PF",]
SGdata <- data[data$Pos=="SG",]
SFdata  <- data[data$Pos=="SF",]

# Filter column for different position
PGdataA <- PGdata[,c("FGptg","AST","PTS","PF","GS")]
CdataA <- Cdata[,c("FGptg","X3Pptg","PF","PTS","GS")]
PFdataA <- PFdata[,c("FGptg","PTS","GS")]
SGdataA <- SGdata[,c("FGptg","X3Pptg","PTS","GS")]
SFdataA <- SFdata[,c("FGptg","PF","PTS","GS")]

# List of data table and name
total = list(PGdataA,CdataA,PFdataA,SGdataA,SFdataA)
Name = list('PG','C','PF','SG','SF')
# Plot 
for (j in 1:5){
  wss <- kmeans(total[[j]],centers=1,nstart=25)$withinss
  for (i in 2:10) wss[i] <- kmeans(total[[j]],centers=i,nstart=25)$tot.withinss
  plot(1:10, wss, type="b", xlab="Number of Clusters",
       ylab="",
       main=paste("The Optimal Number of Clusters for ",Name[[j]]), yaxt='n',
       pch=20, cex=0.8)
  axis(side=1, at=c(0:10))
  title(ylab="Groups sum of squares", line=1, cex.lab=1.2)
}

# Test for different random center
print(c("Pos",c(1:10)))
for(j in 1:5){
  set.seed(11)
  result = Name[[j]]
  km1 <- kmeans(total[[j]],centers=5)
  a_tmp<- km1$cluster
  for(i in 1:10){
    km2 <- kmeans(total[[j]],centers=5)
    b_tmp<- km2$cluster
    result <- c(result,all(b_tmp%in%a_tmp))
  }
  print(result)
}

#interrelated with salary
for(k in 1:5){
  dataset = total[[k]]
  km <- kmeans(dataset,centers=5)$cluster
  IdCluster <- data.frame(id = as.numeric(names(km)), cluster = km)
  DataId <- cbind(dataset,as.numeric(rownames(dataset)))
  names(DataId)[names(DataId)=="as.numeric(rownames(dataset))"] <- "id"
  IdSalary <- merge(DataId,stats,"id")
  Final <- merge(IdSalary,IdCluster,"id")
  Final <- Final[,c("cluster","Salary")]
  ggplot(data=Final,aes(x=cluster,y=Salary)) + geom_point()
}

  

