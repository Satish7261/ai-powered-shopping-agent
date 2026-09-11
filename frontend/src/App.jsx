import {
    useEffect,
    useRef,
    useState,
} from "react";

import {
    MessageCircle,
    Sparkles,
    RotateCcw,
} from "lucide-react";

import Navbar
    from "./components/Navbar";

import Sidebar
    from "./components/Sidebar";

import ChatMessage
    from "./components/ChatMessage";

import TypingIndicator
    from "./components/TypingIndicator";

import ImageUploadModal
    from "./components/ImageUploadModal";

import {
    sendMessage,
    searchByImage,
    checkHealth,
} from "./services/api";


const welcomeMessage = {
    role: "assistant",

    content:
        "Hi! I'm ShopAI 👋\n\n" +
        "Tell me what you're looking for " +
        "and I'll search the store, compare " +
        "ratings, and help you choose the " +
        "right product.\n\n" +
        "You can also upload a product image " +
        "and I'll find similar items.",
};


function App() {

    // -----------------------------
    // State
    // -----------------------------

    const [
        messages,
        setMessages,
    ] = useState([
        welcomeMessage,
    ]);

    const [
        input,
        setInput,
    ] = useState("");

    const [
        loading,
        setLoading,
    ] = useState(false);

    const [
        connected,
        setConnected,
    ] = useState(false);

    const [
        showImageModal,
        setShowImageModal,
    ] = useState(false);


    // -----------------------------
    // References
    // -----------------------------

    const messagesEndRef =
        useRef(null);

    const inputRef =
        useRef(null);


    // -----------------------------
    // Check backend connection
    // -----------------------------

    useEffect(() => {

        const checkBackend = async () => {

            try {

                const data =
                    await checkHealth();

                setConnected(
                    data?.status === "ok"
                );

            } catch (error) {

                console.error(
                    "Health check failed:",
                    error
                );

                setConnected(false);
            }
        };


        // Check immediately
        checkBackend();


        // Check every 30 seconds
        const interval =
            setInterval(
                checkBackend,
                30000
            );


        return () =>
            clearInterval(interval);

    }, []);


    // -----------------------------
    // Scroll to latest message
    // -----------------------------

    useEffect(() => {

        messagesEndRef.current?.scrollIntoView({
            behavior: "smooth",
        });

    }, [
        messages,
        loading,
    ]);


    // -----------------------------
    // Add message
    // -----------------------------

    const addMessage = (
        role,
        content,
        extra = {}
    ) => {

        setMessages(
            (previous) => [

                ...previous,

                {
                    role,
                    content,
                    ...extra,
                },

            ]
        );
    };


    // -----------------------------
    // Send chat message
    // -----------------------------

    const handleSend = async (
        customMessage = null
    ) => {

        const message = (
            customMessage ?? input
        ).trim();


        if (
            !message ||
            loading
        ) {

            return;
        }


        // Clear input
        setInput("");


        // Show user message
        addMessage(
            "user",
            message
        );


        // Start loading
        setLoading(true);


        try {

            const data =
                await sendMessage(
                    message
                );


            console.log(
                "ShopAI response:",
                data
            );


            // Backend returned an error
            if (
                data?.success === false
            ) {

                throw new Error(
                    data?.response ||
                    "Shopping agent returned an error."
                );
            }


            // Display AI response
            addMessage(
                "assistant",
                data?.response ||
                "I couldn't find a response."
            );


            // Backend successfully responded
            setConnected(true);


        } catch (error) {

            console.error(
                "Chat error:",
                error
            );


            // Show the actual error
            addMessage(
                "assistant",
                `ShopAI error: ${
                    error?.message ||
                    "Something went wrong."
                }`
            );


            /*
             * Do NOT mark the backend offline here.
             *
             * The backend can be online while
             * the AI agent itself has an error.
             */
            setConnected(true);

        } finally {

            setLoading(false);


            setTimeout(() => {

                inputRef.current?.focus();

            }, 100);
        }

    };


    // -----------------------------
    // Image search
    // -----------------------------

    const handleImageUpload =
        async (file) => {

        if (
            !file ||
            loading
        ) {

            return;
        }


        // Close modal
        setShowImageModal(false);


        // Show upload message
        addMessage(
            "user",
            "Searching for similar products...",
            {
                imageName:
                    file.name,
            }
        );


        // Start loading
        setLoading(true);


        try {

            const data =
                await searchByImage(
                    file
                );


            console.log(
                "ShopAI image response:",
                data
            );


            if (
                data?.success === false
            ) {

                throw new Error(
                    data?.response ||
                    "Image search failed."
                );
            }


            // Display AI response
            addMessage(
                "assistant",
                data?.response ||
                "I couldn't identify a matching product."
            );


            setConnected(true);


        } catch (error) {

            console.error(
                "Image search error:",
                error
            );


            addMessage(
                "assistant",
                `Image search error: ${
                    error?.message ||
                    "Something went wrong."
                }`
            );


            /*
             * Keep the backend status as online.
             * An image/agent failure does not mean
             * that FastAPI is offline.
             */
            setConnected(true);

        } finally {

            setLoading(false);
        }

    };


    // -----------------------------
    // New conversation
    // -----------------------------

    const clearConversation =
        () => {

        if (loading) {

            return;
        }


        setMessages([
            welcomeMessage,
        ]);


        setInput("");

    };


    // -----------------------------
    // Keyboard handler
    // -----------------------------

    const handleKeyDown =
        (event) => {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            handleSend();
        }

    };


    // -----------------------------
    // UI
    // -----------------------------

    return (

        <div className="app-shell">


            {/* Navbar */}

            <Navbar
                connected={
                    connected
                }
            />


            {/* Application body */}

            <div className="app-body">


                {/* Sidebar */}

                <Sidebar

                    onImageClick={() =>
                        setShowImageModal(
                            true
                        )
                    }

                    onSuggestion={(
                        text
                    ) =>
                        handleSend(
                            text
                        )
                    }

                />


                {/* Chat */}

                <main className="chat-panel">


                    {/* Chat header */}

                    <div className="chat-header">


                        <div className="chat-header-left">


                            <div className="chat-header-icon">

                                <MessageCircle
                                    size={19}
                                />

                            </div>


                            <div>

                                <h2>
                                    AI Shopping Assistant
                                </h2>

                                <p>
                                    Search. Compare.
                                    Shop smarter.
                                </p>

                            </div>

                        </div>


                        {/* New chat */}

                        <button

                            className="new-chat-button"

                            onClick={
                                clearConversation
                            }

                            disabled={
                                loading
                            }

                        >

                            <RotateCcw
                                size={14}
                            />

                            New chat

                        </button>

                    </div>


                    {/* Messages */}

                    <section
                        className="messages-area"
                    >

                        <div
                            className="messages-inner"
                        >

                            {messages.map(
                                (
                                    message,
                                    index
                                ) => (

                                    <ChatMessage
                                        key={
                                            index
                                        }

                                        message={
                                            message
                                        }
                                    />

                                )
                            )}


                            {/* Loading */}

                            {loading && (

                                <TypingIndicator />

                            )}


                            <div
                                ref={
                                    messagesEndRef
                                }
                            />

                        </div>

                    </section>


                    {/* Message composer */}

                    <div className="composer-wrapper">


                        <div className="composer">


                            <button
                                className="composer-ai-icon"
                                type="button"
                            >

                                <Sparkles
                                    size={17}
                                />

                            </button>


                            <textarea

                                ref={
                                    inputRef
                                }

                                value={
                                    input
                                }

                                onChange={(
                                    event
                                ) =>
                                    setInput(
                                        event.target.value
                                    )
                                }

                                onKeyDown={
                                    handleKeyDown
                                }

                                placeholder="Ask ShopAI to find a product..."

                                rows={1}

                                disabled={
                                    loading
                                }

                            />


                            <button

                                className="send-button"

                                onClick={() =>
                                    handleSend()
                                }

                                disabled={
                                    loading ||
                                    !input.trim()
                                }

                                type="button"

                            >

                                <svg
                                    width="17"
                                    height="17"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth="2"
                                >

                                    <path
                                        d="M22 2L11 13"
                                    />

                                    <path
                                        d="M22 2L15 22L11 13L2 9L22 2Z"
                                    />

                                </svg>

                            </button>

                        </div>


                        <p className="composer-disclaimer">

                            ShopAI uses AI to help
                            you discover products.
                            Always review product
                            details before ordering.

                        </p>

                    </div>

                </main>

            </div>


            {/* Image upload modal */}

            {showImageModal && (

                <ImageUploadModal

                    onClose={() =>
                        setShowImageModal(
                            false
                        )
                    }

                    onUpload={
                        handleImageUpload
                    }

                    loading={
                        loading
                    }

                />

            )}

        </div>

    );

}


export default App;