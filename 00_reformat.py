# this step is specific for every collection, since they all come
# in different formats. All texts are to be reformatted into a CSV file
# where columns must have specific information.

# when data is reformatted in this manner, the next script can be applied
# to the folder.

## CSV must be formatted as follows

## URI - uri, must be unique for each piece
## AUT - Author, if available (otherwise empty)
## DAT - Date
## SR1 - Source / Book title
## SR2 - Subsource / Book chapter
## TOP - Topic/Theme, if available (otherwise empty)
## TXT - Text (if title is available, add it to the head of the text as ## title ## ||,
##       newlines as ||)
## MCS1, MSC2, etc - if you have other metadata available, add it into additional
##       columns after the listed ones. Please, provide description of additional
##       metadata (important, if you want to use it )


