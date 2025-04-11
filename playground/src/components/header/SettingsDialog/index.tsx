import { useEffect } from "react"
import { Modal, Tabs } from "antd"
import { useAppSelector } from "@/common"
import styles from "./index.module.scss"

// Import components
import GeneralSettings from "./components/GeneralSettings"
import PromptSettings from "./components/PromptSettings"
import McpSettings from "./components/McpSettings"

// Import hooks
import { useSettingsState } from "./hooks/useSettingsState"
import { useMcpConnection } from "./hooks/useMcpConnection"

const { TabPane } = Tabs

const SettingsDialog = ({ open, onClose }: { open: boolean; onClose: () => void }) => {
    const agentConnected = useAppSelector(state => state.global.agentConnected)

    // Use custom hooks for settings state
    const { settings, dispatch, loadSettings, saveSettings } = useSettingsState()
    const {
        isLoading: mcpLoading,
        connectToMcp,
        listMcpServers
    } = useMcpConnection(settings, dispatch)

    // Load initial settings from localStorage
    useEffect(() => {
        loadSettings()
    }, [])

    // Save settings and dispatch event whenever they change
    useEffect(() => {
        saveSettings(settings)
    }, [settings])

    // Handle MCP connection
    const handleConnectMcp = async () => {
        await connectToMcp()
        await listMcpServers()
    }

    return (
        <Modal
            title="Settings"
            open={open}
            onCancel={onClose}
            footer={null}
            width={600}
            className={styles.settingsDialog}
        >
            <Tabs defaultActiveKey="general">
                <TabPane tab="General" key="general">
                    <GeneralSettings
                        settings={settings}
                        dispatch={dispatch}
                        agentConnected={agentConnected}
                    />
                </TabPane>

                <TabPane tab="Prompt" key="prompt">
                    <PromptSettings
                        settings={settings}
                        dispatch={dispatch}
                        agentConnected={agentConnected}
                    />
                </TabPane>

                <TabPane tab="MCP" key="mcp">
                    <McpSettings
                        settings={settings}
                        dispatch={dispatch}
                        agentConnected={agentConnected}
                        mcpLoading={mcpLoading}
                        onConnectMcp={handleConnectMcp}
                    />
                </TabPane>
            </Tabs>
        </Modal>
    )
}

export default SettingsDialog
