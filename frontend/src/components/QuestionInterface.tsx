import { useState } from "react";
import { MessageSquare, Send, Bot, User } from "lucide-react";
import { api } from "../services/api";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export function QuestionInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content:
        "Hi! I'm your AI assistant. Ask me anything about your codebase and I'll help you understand it better.",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await api.askQuestion(input);
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.answer,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error("❌ Query failed:", error);
      const errorMessage =
        error instanceof Error ? error.message : "Unknown error occurred";
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: `Sorry, I encountered an error: ${errorMessage}\n\nThe AI engine might not be running yet. Make sure:\n1. Backend is running on http://localhost:8000\n2. AI engine is running on http://localhost:8001`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="h-full flex flex-col bg-background">
      {/* Header */}
      <div className="border-b border-border/40 px-6 py-6 backdrop-blur-sm bg-background/80">
        <div className="flex items-center gap-2 animate-fade-in">
          <MessageSquare className="w-5 h-5 text-primary" />
          <h3 className="text-base font-semibold text-foreground">
            Ask Questions
          </h3>
        </div>
        <p className="text-xs text-muted-foreground mt-1">
          Powered by IBM watsonx
        </p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-6 space-y-6">
        {messages.map((message, index) => (
          <div
            key={message.id}
            className="space-y-3 animate-fade-in-up"
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            {message.role === "assistant" && (
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center flex-shrink-0 shadow-lg shadow-primary/20 animate-fade-in">
                  <Bot className="w-4 h-4 text-white" />
                </div>
                <span className="text-sm font-semibold text-foreground">
                  AI Assistant
                </span>
              </div>
            )}
            {message.role === "user" && (
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center flex-shrink-0 border border-border/40">
                  <User className="w-4 h-4 text-muted-foreground" />
                </div>
                <span className="text-sm font-semibold text-foreground">
                  You
                </span>
              </div>
            )}
            <div className="pl-11">
              <p className="text-[15px] leading-relaxed text-foreground/90 p-3 rounded-lg bg-card/50 border border-border/20 hover:border-border/40 transition-all duration-200">
                {message.content}
              </p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="space-y-3 animate-fade-in">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center flex-shrink-0 shadow-lg shadow-primary/20">
                <Bot className="w-4 h-4 text-white animate-pulse" />
              </div>
              <span className="text-sm font-semibold text-foreground">
                AI Assistant
              </span>
            </div>
            <div className="pl-11">
              <div className="flex gap-1.5 p-3 rounded-lg bg-card/50 border border-border/20 w-fit">
                <div
                  className="w-2 h-2 rounded-full bg-primary/60 animate-bounce"
                  style={{ animationDelay: "0ms" }}
                />
                <div
                  className="w-2 h-2 rounded-full bg-primary/60 animate-bounce"
                  style={{ animationDelay: "150ms" }}
                />
                <div
                  className="w-2 h-2 rounded-full bg-primary/60 animate-bounce"
                  style={{ animationDelay: "300ms" }}
                />
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <div className="border-t border-border/40 px-6 py-6 backdrop-blur-sm bg-background/80">
        <form onSubmit={handleSend} className="relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask anything about your codebase..."
            className="w-full px-5 py-4 pr-14 text-[15px] rounded-xl bg-input-background border border-border/50 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 focus:shadow-lg focus:shadow-primary/10 transition-all duration-300 placeholder:text-muted-foreground/60 hover:border-primary/50"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="group absolute right-2.5 top-1/2 -translate-y-1/2 p-2.5 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-200 hover:scale-110 active:scale-95 shadow-lg shadow-primary/20"
          >
            <Send className="w-5 h-5 transition-transform duration-200 group-hover:translate-x-0.5" />
          </button>
        </form>
      </div>
    </div>
  );
}
