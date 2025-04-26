import { useState, useEffect } from "react"
import {
    useAppSelector,
    useAppDispatch,
    apiStartService,
    apiPing,
    GRAPH_NAME_OPTIONS,
    LANG_OPTIONS
} from "@/common"
import { setAgentConnected } from "@/store/reducers/global"
import styles from "./index.module.scss"

let intervalId: any

const ConnectButton = () => {
    const dispatch = useAppDispatch()
    const channel = useAppSelector(state => state.global.options.channel)
    const userId = useAppSelector(state => state.global.options.userId)
    const [mode] = useState("chat")
    const [graphName] = useState(GRAPH_NAME_OPTIONS[2]['value'])
    const [lang] = useState(LANG_OPTIONS[1]['value'])
    const [outputLanguage] = useState(lang)
    const [partialStabilization] = useState(false)
    const [voice] = useState("male")
    const [greeting] = useState("")
    const [mcpSelectedServers] = useState<string[]>([])
    const [mcpApiBase] = useState("")
    const [mcpApiKey] = useState("")
    const [mcpSelectedModel] = useState("")

    // 自動連線功能
    useEffect(() => {
        const autoConnect = async () => {
            try {
                const res = await apiStartService({
                    channel,
                    userId,
                    language: lang,
                    voiceType: voice,
                    graphName: graphName,
                    mode: mode,
                    outputLanguage: outputLanguage,
                    partialStabilization: partialStabilization,
                    greeting: greeting,
                    mcpSelectedServers: mcpSelectedServers.join(','),
                    mcpApiBase: mcpApiBase,
                    mcpApiKey: mcpApiKey,
                    mcpModel: mcpSelectedModel
                })

                if (res?.code === 0) {
                    dispatch(setAgentConnected(true))
                    startPing()
                }
            } catch (error) {
                console.error("Auto connect failed:", error)
                // 如果連線失敗，5秒後重試
                setTimeout(autoConnect, 5000)
            }
        }

        // 組件掛載時自動連線
        autoConnect()

        // 組件卸載時清理
        return () => {
            if (intervalId) {
                clearInterval(intervalId)
                intervalId = null
            }
        }
    }, []) // 只在組件掛載時執行一次

    const startPing = () => {
        if (intervalId) {
            clearInterval(intervalId)
        }
        intervalId = setInterval(() => {
            apiPing(channel)
        }, 3000)
    }

    // 移除按鈕的渲染，因為不需要手動控制連線狀態
    return null
}

export default ConnectButton

