/**
 * Enum representing the type of the chat message.
 * Possible values are 'user' or 'agent'.
 */
enum MessageType {
  User = 'user',
  Agent = 'agent',
}

/**
 * Interface representing a chat message.
 * Contains three properties: type (which is of type MessageType), content (a string), and timestamp (a Date object).
 */
interface ChatMessage {
  type: MessageType;
  content: string;
  timestamp: Date;
}

/**
 * Function to create a new chat message.
 * @param type - The type of the chat message. Must be either 'user' or 'agent'.
 * @param content - The content of the chat message. Can be any string.
 * @returns A new chat message object that conforms to the ChatMessage interface.
 */
function createChatMessage(type: MessageType, content: string): ChatMessage {
  // Create and return a new chat message object with the given type and content,
  // and a current timestamp.
  return {
    type,
    content,
    timestamp: new Date(),
  };
}

/**
 * Example usage of the createChatMessage function.
 * Creates a new chat message object with a type of 'user' and some example content.
 * The new object is stored in the variable userMessage.
 */
const userMessage = createChatMessage(MessageType.User, 'Hello, how can I help you?');

/**
 * Logs the new chat message object to the console.
 * The output will include the message type, content, and timestamp.
 */
console.log(userMessage);
