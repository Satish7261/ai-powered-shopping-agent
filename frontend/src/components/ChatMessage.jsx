import {
    Bot,
    User,
    Sparkles,
} from "lucide-react";



function cleanText(text) {

    if (!text) {

        return "";

    }


    return text

        .replace(/```/g, "")

        .replace(/\*\*/g, "")

        .replace(/\\\$/g, "$")

        .trim();

}



function ChatMessage({
    message,
}) {

    const isUser =
        message.role === "user";


    return (

        <div
            className={
                `message-row ${
                    isUser
                        ? "user-message-row"
                        : "assistant-message-row"
                }`
            }
        >


            {/* Avatar */}

            <div
                className={
                    `avatar ${
                        isUser
                            ? "user-avatar"
                            : "ai-avatar"
                    }`
                }
            >

                {

                    isUser

                        ? (
                            <User
                                size={16}
                            />
                        )

                        : (
                            <Bot
                                size={17}
                            />
                        )

                }

            </div>



            {/* Message */}

            <div
                className={
                    `message-container ${
                        isUser
                            ? "user-message-container"
                            : "assistant-message-container"
                    }`
                }
            >


                {!isUser && (

                    <div className="ai-message-label">

                        <Sparkles
                            size={12}
                        />

                        <span>
                            ShopAI
                        </span>

                    </div>

                )}



                <div
                    className={
                        `message-bubble ${
                            isUser
                                ? "user-bubble"
                                : "ai-bubble"
                        }`
                    }
                >

                    {cleanText(
                        message.content
                    )}

                </div>



                {message.imageName && (

                    <div className="image-message-label">

                        📷 {message.imageName}

                    </div>

                )}


            </div>


        </div>

    );

}


export default ChatMessage;