// runner_utils.h: Utility functions for the runner.

#ifndef RUNNER_UTILS_H_
#define RUNNER_UTILS_H_

// Includes
#include <string>  // for std::string
#include <vector>  // for std::vector

//------------------------------------------------------------------------------
// Name: CreateAndAttachConsole
//
// Description:
//   Creates a console for the process and redirects stdout and stderr to it
//   for both the runner and the Flutter library.
//
//------------------------------------------------------------------------------
void CreateAndAttachConsole();

//------------------------------------------------------------------------------
// Name: Utf8FromUtf1
