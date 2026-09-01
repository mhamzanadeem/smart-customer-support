type Props = {
  message: {
    role: "user" | "assistant";
    content: string;
    agent?: string;
    category?: string;
    sources?: string[];
  };
};

export default function Message({
  message,
}: Props) {
  return (
    <div
      className={`message ${message.role}`}
    >
      <div className="bubble">
        <strong>
          {message.role === "user"
            ? "You"
            : "AI Support"}
        </strong>

        <p>{message.content}</p>

        {message.role ===
          "assistant" && (
          <small>
            Agent: {message.agent}
            {" · "}
            Category: {message.category}
          </small>
        )}

        {message.sources &&
          message.sources.length >
            0 && (
            <div className="sources">
              Sources:{" "}
              {message.sources.join(
                ", "
              )}
            </div>
          )}
      </div>
    </div>
  );
}