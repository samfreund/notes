
data <- read.csv("~/notes/math/2480/labs/lab1/data.csv")

summary(data)
# 1: Single categorical variable
# a) Frequency table for Color with relative frequency
color_freq <- table(data$Color)
color_rel_freq <- prop.table(color_freq)
color_table <- data.frame(
	Color = names(color_freq),
	Frequency = as.vector(color_freq),
	RelativeFrequency = as.vector(color_rel_freq)
)
color_table

# b) Appropriate plot: bar chart of counts (or relative frequencies)

# c) Bar chart of Color counts
barplot(
	color_freq,
	main = "Car Color Frequency",
	xlab = "Color",
	ylab = "Frequency",
	col = "steelblue"
)

# 2: One quantitative variable

# a) Mean and variance of Price
price_mean <- mean(data$Price, na.rm = TRUE)
price_var <- var(data$Price, na.rm = TRUE)
price_mean
price_var

# b) Five-number summary for Price
price_fivenum <- fivenum(data$Price, na.rm = TRUE)
price_fivenum

# c) Box plot of Price and outliers
price_box <- boxplot(data$Price, main = "Boxplot of Price", ylab = "Price")
price_outliers <- price_box$out
price_outliers

# d) Log transform of Price (new column named "log(Price)")
data$`log(Price)` <- log(data$Price)

# e) Box plot of log(Price) and outliers
log_price_box <- boxplot(data$`log(Price)`, main = "Boxplot of log(Price)", ylab = "log(Price)")
log_price_outliers <- log_price_box$out
log_price_outliers

# f) Histograms for Price and log(Price)
hist(data$Price, main = "Histogram of Price", xlab = "Price", col = "lightgray")
hist(data$`log(Price)`, main = "Histogram of log(Price)", xlab = "log(Price)", col = "lightgray")

# g) Five-number summary for Price with outliers removed
price_no_outliers <- data$Price[!(data$Price %in% price_outliers)]
price_no_outliers_fivenum <- fivenum(price_no_outliers, na.rm = TRUE)
price_no_outliers_fivenum
