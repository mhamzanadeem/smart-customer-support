import Chat from "./components/Chat";

export default function Home() {
  return (
    <main className="container">
      <header>
        <h1>Smart Customer Support</h1>

        <p>
          AI-powered support using RAG,
          LangGraph, Agents SDK and MCP.
        </p>
      </header>

      <Chat />
    </main>
  );
}