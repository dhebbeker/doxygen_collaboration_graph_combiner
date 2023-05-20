# doxygen_collaboration_graph_combiner
Scripts to combine (all) collaboration graphs generated by doxygen to one.

## Objective

These scripts shall help to combine collaboration graphs, which were generated by doxygen, to one combined graph.

Doxygen can generate collaboration graphs for every class.
Sometimes it can be helpful to have a collaboration graph for more than just that class.

## Mechanics

The scripts uses the DOT files for the collaboration graphs generated by doxygen.
It creates DOT files where the the nodes in the graphs have been renamed such that they correspond to their content.
Then the graphs are combined to one.

## System requirements

 - doxygen
 - Python
 - dot / GraphViz

## Perquisites

The following options must be set when running doxygen:

```
HAVE_DOT            = YES
COLLABORATION_GRAPH = YES
DOT_CLEANUP         = NO
```

## Steps

 1. Generate the documentation with doxygen.
    A clean rebuild may be necessary to create the intermediate DOT files.  
    ```.sh
    rm -r html/
    doxygen
    ```
 2. Prepare the files:  
    The original files are not modified.  
    ```.sh
    python3 prepare_files.py html/*__coll__*.dot
    ```
 3. Combine graphs:  
    Instead of using all altered files, one may also select only a subset.  
    ```.sh
    python3 merge_digraphs.py html/*_renamed.dot combined__coll__.dot
    ```
 4. Generate diagram:  
    ```.sh
    dot -O -Tsvg combined__coll__.dot
    ```

