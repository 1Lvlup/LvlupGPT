class Stack<T> {
  // A private list to store the elements in the stack
  final List<T> _list = [];

  // Adds an element to the top of the stack
  void push(T element) {
    // Add the element to the end of the list
    _list.add(element);
  }

  // Removes and returns the top element from the stack
  T pop() {
    // Get the last element in the list
    var element = _list.last;
    
    // Remove the last element from the list
    _list.removeLast();
    
    // Return the removed element
    return element;
  }

  // Returns the top element of the stack without removing it
  T peek() {
    // Return the last element in the list
    return _list.last;
  }

  // Check if the stack is empty
  bool get isEmpty => _list.isEmpty;

  // Check if the stack is not empty
  bool get isNotEmpty => _list.isNotEmpty;
}

