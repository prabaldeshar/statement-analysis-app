import { Spinner } from "@/components/ui/spinner";
import { CheckCircle2, X, RefreshCcw, Close } from "lucide-react";

export default function ProcessingStatus({taskStatus="SUCCESS", taskMessage="The processing is complete", handlesetTaskStatus}) {
    return (
        <div className="flex justify-center  md:right-8 md:top-8">
            <div className="bg-white p-2 rounded-lg shadow-lg text-center space-y-4 max-w-md">
                {taskStatus === "PENDING" && (
                    <>
                        <div className="flex justify-center">
                            <Spinner/>
                        </div>
                        <p className="text-lg">Processing your statement...</p>
                    </>
                )}

                {taskStatus === "SUCCESS" && (
                    <div className="flex flex-col items-center">                     
                        <div className="flex justify-center text-green-500 ">
                            <CheckCircle2 className="w-10 h-10" />
                        </div>
                        <p className="text-md text-gray-700 my-2">{taskMessage}</p>
                        <button 
                            className="px-3 py-2 text-md bg-green-100 text-black  rounded-lg hover:bg-green-200 transition-all flex justify-center gap-2"
                            onClick={() => window.location.reload()}
                        >
                            
                            Refresh
                            <RefreshCcw className="w-5 h-5" />
                        </button>
                    </ div>
                )}

                {taskStatus === "FAILED" && (
                    <div className="flex flex-col items-center">
                        <div className="flex justify-center text-red-500">
                            <X className="w-10 h-10" />
                        </div>
                        <p className="text-md text-gray-700 my-2">{taskMessage}</p>
                        <button
                            className="px-3 py-2 bg-red-100 text-black  rounded-lg hover:bg-red-200 transition-all flex justify-center gap-2"
                            onClick={() => handlesetTaskStatus(null)}
                        >
                            Close
                            <X className="w-5 h-5"/>
                        </button>
                    </ div>
                )}
            </div>
        </div>
    );
}
