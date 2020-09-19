df <- read.csv("",stringsAsFactors = FALSE)
colnames(df) <- c("Genre", "Number")
theme_custom <- function() {
  theme_minimal() %+replace%
    theme(
      panel.grid.major  = element_line(color = "white"),
      panel.background = element_rect(fill = "snow1"),
      panel.border = element_rect(color = "black", fill = NA),
      axis.line = element_line(color = "grey25"),
      axis.ticks = element_line(color = "grey25"),
      axis.text = element_text(color = "grey25")
    )
}

df <- arrange(df,desc(Number)) %>% top_n(10,Number)
ggplot(df,aes(Genre,Number),col = "grey") + geom_bar(stat="identity",fill="dodgerblue4") +
  labs(title = "Superhero movies genres", y= "Number of movies in genre", x = "Genres", caption="Data from imdb.com, 200 most voted movies based on comic books") +
 theme_custom()+ theme(title = element_text(family = "serif", face='bold', size = 14),axis.text.x = element_text(angle=35))+
  scale_y_continuous(breaks=seq(0,120,15)) +coord_flip()
