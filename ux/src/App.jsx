import { useState } from 'react';
import axios from 'axios';  // Import Axios
import './App.css';
import chatbot from '../public/chatbot.svg'
import send from '../public/send.svg'
import close from '../public/close.svg'
function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
 const [isOpen, setIsopen] = useState(false)
  const sendMessage = async (e) => {
    e.preventDefault();
    if (input.trim()) {
      // Add the user's message to the chat
      setMessages([...messages, { text: input, sender: 'user' }]);

      // Clear the input field
      setInput('');

      try {
        // Make an Axios call to your backend API
        const response = await axios.post('https://bumble.free.beeceptor.com', {
          message: input,
        });

        // Add the response from the backend to the chat
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: response.data.reply, sender: 'bot' },
        ]);
      } catch (error) {
        console.error('Error sending message:', error);
        // Optionally, handle the error, e.g., show an error message in the chat
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: 'Error sending message. Please try again.', sender: 'bot' },
        ]);
      }
    }
  };

  return (
    <div className="bg-gray-300 relative w-screen h-screen back">
      <button className={`${isOpen ? "hidden -z-0" : "flex z-20"} rounded-full p-8 bg-[#2258A9] items-center justify-center hover:scale-105 transition-all duration-300 cursor-pointer absolute bottom-8 right-8  border-2 border-white/50 shadow-2xl`} onClick={()=>setIsopen(true)}> <img src={chatbot} className='w-12 h-12 object-cover'/></button>
      <div className={`${isOpen ? "translate-y-0 opacity-100 z-10" : "-translate-y-50 opacity-0 -z-0 "}  max-w-md mx-auto bg-white rounded-xl shadow-md flex flex-col absolute bottom-16 right-16 transition-all duration-300 ease-in-out overflow-hidden w-[600px]`}>
        <div className='flex px-6 py-6 items-center bg-gray-100 justify-between'>
          <h4 className='font-bold text-2xl '>Chat Bot</h4>

          <button onClick={() => setIsopen(false)} className='p-4 hover:bg-gray-300 rounded-full transition-all duration-300 ease-in-out cursor-pointer'>
           <img src={close} className='w-6 h-6 object-cover  '/>
          </button>
        </div>
        <div className="overflow-y-auto p-4 p min-[300px] h-[50vh] max-h-[600px] flex flex-col gap-8 ">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`py-4 px-4 w-fit max-w-[400px] rounded-lg ${message.sender === 'user' ? 'bg-[#2258A9] text-white self-end ml-auto rounded-br-sm' : 'bg-gray-300 self-start mar-auto rounded-bl-sm'}`}
            >
              {message.text}
            </div>
          ))}
        </div>
        <form onSubmit={sendMessage} className="flex m-4">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-1 p-2 focus:py-3 transition-all duration-300 border-2 border-gray-200 rounded-l-lg focus:outline-none focus:border-[#2258A9]"
            placeholder="Type your message..."
          />
          <button type="submit" className="bg-[#2258A9] text-white py-2 px-4 rounded-r-lg flex items-center gap-2">
            Send
            <img src={send} className='w-4 h-4 object-cover '/>
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
