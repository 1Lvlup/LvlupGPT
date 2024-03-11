/**
 * Enum representing the type of the chat message.
 */
enum MessageType {
  User = 'user',
  Agent = 'agent',
}

/**
 * Interface representing a chat message.
 */
interface ChatMessage {
  type: MessageType;
  content: string;
  timestamp: Date;
}

/**
 * Function to create a new chat message.
 * @param type - The type of the chat message.
 * @param content - The content of the chat message.
 * @returns A new chat message.
 */
function createChatMessage(type: MessageType, content: string): ChatMessage {
  return {
    type,
    content,
    timestamp: new Date(),
  };
}

/**
 * Example usage of the createChatMessage function.
 */
const userMessage = createChatMessage(MessageType.User, 'Hello, how can I help you?');
console.log(userMessage);
