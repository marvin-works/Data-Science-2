set.seed(1)

# Generate random numbers and store it in a variable called data
data = runif(20, 1, 10)
data

# Calculate mean
mean = mean(data)
print(mean)

# Calculate median
median = median(data)
print(median)

# Create a function for calculating mode
mode <- function(x) {
    ux <- unique(x)
    ux[which.max(tabulate(match(x, ux)))]
}

result <- mode(data)

print(data)

cat("Mode =", result, "\n")

# Calculate variance and std Deviation
variance = var(data)
standardDeviation = sqrt(var(data))
print(standardDeviation)

# Calculate median
median = median(data)
print(median)