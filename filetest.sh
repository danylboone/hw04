#!/bin/bash

if [ $# == 0 ]
then
  echo "You have not provided any arguments. You
  must provide at least 1!"
  echo "filetest.sh"
  echo "Usage: filetest.sh filename1 [filename2,filename3,...]"
  echo " "
else
  for file in $*; do
      echo "Testing to see if $file exists..."
      
      # Does it exist?
      if [ -e $file ]; then
	  comment="$file exists!"
	  # Save permissions to a variable.
	  perms=$(ls -ld -- "$file" | awk '{print $1}')
      else
	  comment="Sorry, $file does not exist."
	  echo "$comment"
      fi
      
      # Type of file
      if [ -d "$file" ]; then
	  comment2="and it is a directory."
	  echo "$comment $comment2"
	  echo "Permissions: $perms"
      elif [ -f "$file" ]; then
	  comment2="and it is a regular file."
	  echo "$comment $comment2"
	  echo "Permission: $perms"

	  if [ -s "$file" ]; then
	      echo "File is NOT blank."
	  else 
	      echo "File is blank."
	  fi
    
      else
	  comment2="but it is not a regular file or a directory."
	  echo "$comment $comment2"
          echo "Permissions: $perms"                            
      fi
      
      echo " "
  done
fi