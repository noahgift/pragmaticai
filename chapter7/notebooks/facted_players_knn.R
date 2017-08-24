player_cluster <- read_csv("~/src/aibook/src/chapter7/data/../data/nba_2017_players_social_with_clusters.csv", 
                         col_types = cols(X1 = col_skip()))
library("ggplot2")

#Name Clusters
player_cluster$cluster_name[player_cluster$cluster == 0] <- "Low Pay/Low Performance"
player_cluster$cluster_name[player_cluster$cluster == 1] <- "High Pay/Above Average Performance"
player_cluster$cluster_name[player_cluster$cluster == 2] <- "Low Pay/Average Performance"
player_cluster$cluster_name[player_cluster$cluster == 3] <- "High Pay/High Performance"
player_cluster$cluster_name[player_cluster$cluster == 4] <- "Medium Pay/Above Average Performance"

#Create faceted plot
p <- ggplot(data = player_cluster) +
    geom_point(mapping = aes(x = WINS_RPM,
                             y = POINTS, 
                             color = SALARY_MILLIONS, 
                             size = PAGEVIEWS))+
    facet_wrap(~ cluster_name) +
    ggtitle("NBA Players 2016-2017 Faceted Plot of Social Power and Performance") +
    ylab("POINTS PER GAME") +
    xlab("WINS ATTRIBUTABLE TO PLAYER (WINS_RPM)") + 
    geom_text(aes(x = WINS_RPM, y = POINTS, label=ifelse(PAGEVIEWS>10000|TOV>5|AGE>37|WINS_RPM>15|cluster == 2 & WINS_RPM > 3,
                                                         as.character(PLAYER),'')),hjust=.8, check_overlap = FALSE)    

#Change legends
p + 
    guides(color = guide_legend(title = "Salary Millions")) +
    guides(size = guide_legend(title = "Wikipedia Daily Pageviews" ))+
    scale_color_gradientn(colours = rainbow(3))



