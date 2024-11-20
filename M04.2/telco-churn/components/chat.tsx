'use client'
import { useState } from "react";
import { RefreshCcw, Send } from "lucide-react";
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

type ChatResponse = {
  cleaned_sql_query?: string;
  error?: string;
  llm_response?: string;
}

export default function Chatcomponent() {
  const [inputMessage, setInputMessage] = useState<string>(''); 
  const [isLoading, setIsLoading] = useState<boolean>(false); 
  const [assistantResponse, setAssistantResponse] = useState<string>(''); 
  const [sqlQuery, setSqlQuery] = useState<string>(''); 
  const [selectedModel, setSelectedModel] = useState<string>('gemma2-9b-it');

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    setIsLoading(true);
    setSqlQuery(''); // Reset SQL query on new request
    setAssistantResponse('');

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: [{ role: 'user', content: inputMessage }],
          model: selectedModel,
        })
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data: ChatResponse = await response.json();

      if (data.error) {
        setAssistantResponse(`Error: ${data.error}`);
      } else if (data.cleaned_sql_query) {
        setSqlQuery(data.cleaned_sql_query); // Display the cleaned SQL query
      } else {
        setAssistantResponse('Received an unexpected response format');
      }
    } catch (error) {
      console.error('Error:', error);
      setAssistantResponse('Sorry, there was an error processing your request.');
    } finally {
      setInputMessage('');
      setIsLoading(false);
    }
  };

  return (  
    <div className="flex-1 flex flex-col justify-between p-4 max-w-4xl mx-auto w-full">
      {/* Input Area */}
      <div className="flex items-center space-x-2 mb-4">
        <Input 
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Ask a question about your database..."
          className="flex-1"
        />
        
        {/* Model Selection Dropdown */}
        <select
          value={selectedModel}
          onChange={(e) => setSelectedModel(e.target.value)}
          className="border rounded p-2"
        >
          <option value="gemma2-9b-it">gemma2-9b-it</option>
          <option value="llama3-groq-70b-8192-tool-use-preview">llama3-groq-70b-8192-tool-use-preview</option>
          <option value="llama-3.1-70b-versatile">llama-3.1-70b-versatile</option>
          <option value="llama-3.1-70b-specdec">llama-3.1-70b-specdec</option>
          <option value="llama-3.1-8b-instant">llama-3.1-8b-instant</option>
          <option value="llama-3.2-3b-preview">llama-3.2-3b-preview</option>
          <option value="llama3-70b-8192">llama3-70b-8192</option>
        </select>
        
        <Button 
          onClick={sendMessage} 
          disabled={isLoading}
        >
          {isLoading ? (
            <RefreshCcw className="mr-2 h-4 w-4 animate-spin" />
          ) : (
            <Send className="h-4 w-4" />
          )}
        </Button>
      </div>

      {/* SQL Query Display */}
      {sqlQuery && (
        <Card className="mb-4 bg-gray-50">
          <CardContent className="p-4">
            <div className="font-bold mb-2">SQL Query:</div>
            <pre className="bg-gray-100 p-2 rounded overflow-x-auto text-sm">
              {sqlQuery}
            </pre>
          </CardContent>
        </Card>
      )}

      {/* Assistant Response */}
      {assistantResponse && (
        <Card className="mb-4 bg-gray-50 self-start">
          <CardContent className="p-4">
            {assistantResponse}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
