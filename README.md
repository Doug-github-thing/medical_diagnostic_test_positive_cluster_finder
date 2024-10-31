# medical_diagnostic_test_positive_cluster_finder
An algorithm for finding clusters of positive results on a 96-well plate. Helpful for evaluating possible cross contamination of biological sample in the context of a medical lab diagnostic assay.

A cluster is defined as 3 or more positive results adjacent to one another. In practice, having a group of positive results close to one another could be an inidcation that these samples could be cross contaminated during the process of testing, meaning they all should be retested for confirmation.

This is a toy model, which automatically generates randomized result data for test samples with ids from 1 to 96. It then iterates through the sample results, one at a time until it finds a positive result. It then uses a BFS algorithm to find how many adjancent positives there are. If it's 3 or more, it counts this as a cluster. If not, it does not. But it will not check these samples again, as it goes back to iterating through the rest of the samples, checking each exactly once.

This should run in linear time, since it checks every sample exactly once. If there are no positives, there is no BFS analysis at all since it only triggers once hitting the first positive. Once the BFS begins, there is a constant time cost for each positive it checks, as it checks for all adjacent samples that have not yet been either queued or visited yet.
