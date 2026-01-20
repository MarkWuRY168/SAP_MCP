// 全局变量
let currentTool = null;
let originalTools = [];
let configData = null;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 加载配置数据
    loadConfigData();
    
    // 绑定事件监听器
    bindEventListeners();
    
    // 绑定导航事件
    bindNavigationListeners();
    
    // 默认切换到服务管理页面
    switchPage('服务管理');
});

// 加载工具列表
async function loadToolList() {
    try {
        const response = await axios.get('/api/tools');
        const result = response.data;
        
        if (result.RESULT && Array.isArray(result.RESULT)) {
            originalTools = result.RESULT;
            renderToolList(originalTools);
        } else {
            displayError('加载工具列表失败: 无效的数据格式');
        }
    } catch (error) {
        console.error('加载工具列表失败:', error);
        displayError('加载工具列表失败: ' + (error.response?.data?.detail || error.message));
    }
}

// 渲染工具列表
function renderToolList(tools) {
    const toolList = document.getElementById('toolList');
    
    if (tools.length === 0) {
        toolList.innerHTML = `
            <div class="text-center py-4">
                <h5>未找到工具</h5>
                <p class="text-muted">没有匹配的工具或服务器连接失败</p>
            </div>
        `;
        return;
    }
    
    toolList.innerHTML = tools.map(tool => `
        <a href="#" class="list-group-item list-group-item-action" data-tool-id="${tool.TOOL_ID}">
            <h6 class="mb-1">${tool.TOOL_ID}</h6>
            <small class="text-muted">${tool.DESCRIPTION || '无描述'}</small>
        </a>
    `).join('');
    
    // 绑定工具点击事件
    toolList.querySelectorAll('.list-group-item').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            // 移除其他项的激活状态
            toolList.querySelectorAll('.list-group-item').forEach(i => i.classList.remove('active'));
            // 添加当前项的激活状态
            this.classList.add('active');
            
            const toolId = this.getAttribute('data-tool-id');
            loadToolDetails(toolId);
        });
    });
}

// 加载工具详情
async function loadToolDetails(toolId) {
    try {
        const response = await axios.post(`/api/tools/${toolId}/details`);
        let result = response.data;
        
        if (result && result.PARAM) {
            // 从缓存的工具列表中查找描述
            const toolFromList = originalTools.find(tool => tool.TOOL_ID === toolId);
            if (toolFromList && toolFromList.DESCRIPTION) {
                // 将描述添加到工具详情中
                result.DESCRIPTION = toolFromList.DESCRIPTION;
            }
            
            currentTool = {
                id: toolId,
                details: result
            };
            renderToolDetails(result);
            generateToolForm(result.PARAM);
        } else {
            displayError('加载工具详情失败: 无效的数据格式');
        }
    } catch (error) {
        console.error('加载工具详情失败:', error);
        displayError('加载工具详情失败: ' + (error.response?.data?.detail || error.message));
    }
}

// 渲染工具详情
function renderToolDetails(details) {
    const toolDetails = document.getElementById('toolDetails');
    
    toolDetails.innerHTML = `
        <h5>${details.TOOL_NAME || '工具详情'}</h5>
        <p class="text-muted mb-3">工具ID: ${details.TOOL_ID}</p>
        
        <div class="mb-4">
            <h6>描述</h6>
            <p>${details.DESCRIPTION || '无描述信息'}</p>
        </div>
        
        <div class="mb-4">
            <h6>参数说明</h6>
            <p class="text-muted">请在下方表单中配置工具参数</p>
        </div>
        
        <div>
            <h6>工具信息</h6>
            <table class="table table-sm table-bordered">
                <tbody>
                    <tr>
                        <th>工具ID</th>
                        <td>${details.TOOL_ID}</td>
                    </tr>
                    <tr>
                        <th>工具名称</th>
                        <td>${details.TOOL_NAME || '-'}</td>
                    </tr>
                    <tr>
                        <th>接口版本</th>
                        <td>${details.VERSION || '-'}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    `;
}

// 生成工具参数表单
function generateToolForm(paramSchema) {
    const toolForm = document.getElementById('toolForm');
    const toolUsage = document.getElementById('toolUsage');
    
    // 如果没有参数schema，显示简单表单
    if (!paramSchema || typeof paramSchema !== 'object') {
        toolForm.innerHTML = `
            <div class="text-center py-3">
                <p class="text-muted">该工具无需配置参数</p>
            </div>
        `;
        toolUsage.style.display = 'block';
        return;
    }
    
    // 递归生成表单字段
    function generateFields(schema, parentPath = '') {
        let html = '';
        
        for (const [key, value] of Object.entries(schema)) {
            const fieldName = parentPath ? `${parentPath}[${key}]` : key;
            
            if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
                // 嵌套对象
                html += `
                    <div class="mb-4">
                        <h6 class="text-primary">${key}</h6>
                        <div class="ps-3 border-start border-primary">
                            ${generateFields(value, fieldName)}
                        </div>
                    </div>
                `;
            } else if (Array.isArray(value)) {
                // 数组（暂时显示为文本框）
                html += `
                    <div class="mb-3">
                        <label for="${fieldName}" class="form-label">${key} (数组)</label>
                        <textarea class="form-control" id="${fieldName}" name="${fieldName}" rows="3" placeholder="请输入JSON格式的数组"></textarea>
                        <div class="form-text">例如: ["value1", "value2"]</div>
                    </div>
                `;
            } else {
                // 基本类型
                html += `
                    <div class="mb-3">
                        <label for="${fieldName}" class="form-label">${key}</label>
                        <input type="text" class="form-control" id="${fieldName}" name="${fieldName}" placeholder="${typeof value === 'string' ? value : JSON.stringify(value)}" value="${typeof value === 'string' ? value : ''}">
                        <div class="form-text">类型: ${typeof value}, 默认值: ${JSON.stringify(value)}</div>
                    </div>
                `;
            }
        }
        
        return html;
    }
    
    toolForm.innerHTML = generateFields(paramSchema);
    toolUsage.style.display = 'block';
}

// 执行工具
async function executeTool() {
    if (!currentTool) {
        displayError('请先选择一个工具');
        return;
    }
    
    try {
        // 获取表单数据
        const formData = new FormData(document.getElementById('toolForm'));
        const params = {};
        
        // 转换表单数据为JSON对象
        for (const [name, value] of formData.entries()) {
            // 解析嵌套字段
            const keys = name.match(/[\w]+/g);
            if (keys) {
                let current = params;
                for (let i = 0; i < keys.length - 1; i++) {
                    const key = keys[i];
                    if (!current[key]) current[key] = {};
                    current = current[key];
                }
                current[keys[keys.length - 1]] = parseValue(value);
            }
        }
        
        // 显示加载状态
        showExecutionResult('加载中...', true);
        
        // 执行工具
        const response = await axios.post(`/api/tools/${currentTool.id}/use`, params);
        
        // 显示结果
        showExecutionResult(JSON.stringify(response.data, null, 2));
    } catch (error) {
        console.error('执行工具失败:', error);
        showExecutionResult('执行失败: ' + (error.response?.data?.detail || error.message), true);
    }
}

// 解析表单值
function parseValue(value) {
    // 尝试解析JSON
    try {
        return JSON.parse(value);
    } catch {
        // 如果不是JSON，返回原始值
        return value;
    }
}

// 显示执行结果
function showExecutionResult(result, isError = false) {
    const executionResult = document.getElementById('executionResult');
    const resultOutput = document.getElementById('resultOutput');
    
    resultOutput.textContent = result;
    resultOutput.className = isError ? 'bg-danger text-white p-3 rounded' : 'bg-light p-3 rounded';
    executionResult.style.display = 'block';
    
    // 滚动到结果区域
    executionResult.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// 绑定导航事件监听器
function bindNavigationListeners() {
    // 获取所有导航链接
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // 移除所有导航链接的激活状态
            navLinks.forEach(navLink => navLink.classList.remove('active'));
            
            // 添加当前导航链接的激活状态
            this.classList.add('active');
            
            // 获取要切换的页面名称
            const pageName = this.textContent.trim();
            
            // 切换页面
            switchPage(pageName);
        });
    });
}

// 页面切换函数
function switchPage(pageName) {
    // 隐藏所有页面
    document.getElementById('toolsPage').style.display = 'none';
    document.getElementById('configPage').style.display = 'none';
    document.getElementById('servicePage').style.display = 'none';
    document.getElementById('logsPage').style.display = 'none';
    
    // 显示对应的页面
    if (pageName === '工具管理') {
        document.getElementById('toolsPage').style.display = 'block';
        // 加载工具列表
        loadToolList();
    } else if (pageName === '服务器配置') {
        document.getElementById('configPage').style.display = 'block';
        // 确保配置数据已加载
        if (!configData) {
            loadConfigData();
        }
    } else if (pageName === '服务管理') {
        document.getElementById('servicePage').style.display = 'block';
        // 加载服务状态
        loadServiceStatus();
    } else if (pageName === '日志查看') {
        document.getElementById('logsPage').style.display = 'block';
        // 加载日志
        loadLogs();
    }
}

// 加载配置数据
async function loadConfigData() {
    try {
        const response = await axios.get('/api/config');
        const result = response.data;
        
        if (result.config && result.sap_config) {
            configData = {
                sap: result.sap_config,
                mcp: result.config
            };
            renderConfigForm();
        } else {
            console.error('加载配置数据失败: 无效的数据格式');
        }
    } catch (error) {
        console.error('加载配置数据失败:', error);
    }
}

// 渲染配置表单
function renderConfigForm() {
    if (!configData) return;
    
    // 设置SAP配置
    document.getElementById('sapBaseUrl').value = configData.sap.base_url;
    document.getElementById('sapClientId').value = configData.sap.client_id;
    document.getElementById('sapUser').value = configData.sap['sap-user'];
    document.getElementById('sapPassword').value = configData.sap['sap-password'];
    document.getElementById('sapTimeout').value = configData.sap.timeout;
    
    // 设置MCP服务器配置
    document.getElementById('mcpHost').value = configData.mcp.host;
    document.getElementById('mcpPort').value = configData.mcp.port;
    document.getElementById('mcpPath').value = configData.mcp.path;
}

// 加载服务状态
async function loadServiceStatus() {
    try {
        const response = await axios.get('/api/service/status');
        const status = response.data;
        renderServiceStatus(status);
    } catch (error) {
        console.error('加载服务状态失败:', error);
        showServiceMessage('加载服务状态失败: ' + (error.response?.data?.detail || error.message), 'danger');
    }
}

// 渲染服务状态
function renderServiceStatus(status) {
    // 更新状态文本和样式
    const statusText = document.getElementById('serviceStatusText');
    statusText.textContent = status.status === 'running' ? '运行中' : '已停止';
    statusText.className = status.status === 'running' ? 'fs-4 fw-bold text-success' : 'fs-4 fw-bold text-danger';
    
    // 更新主机和端口
    document.getElementById('serviceHost').textContent = status.host;
    document.getElementById('servicePort').textContent = status.port;
    
    // 更新进程ID
    const pidContainer = document.getElementById('servicePidContainer');
    const pidElement = document.getElementById('servicePid');
    if (status.pid) {
        pidContainer.style.display = 'block';
        pidElement.textContent = status.pid;
    } else {
        pidContainer.style.display = 'none';
    }
    
    // 更新错误信息
    const errorContainer = document.getElementById('serviceErrorContainer');
    const errorElement = document.getElementById('serviceError');
    if (status.error) {
        errorContainer.style.display = 'block';
        errorElement.textContent = status.error;
    } else {
        errorContainer.style.display = 'none';
    }
}

// 启动服务
async function startService() {
    try {
        // 禁用按钮，防止重复点击
        const startBtn = document.getElementById('startServiceBtn');
        const stopBtn = document.getElementById('stopServiceBtn');
        startBtn.disabled = true;
        stopBtn.disabled = true;
        
        showServiceMessage('正在启动服务...', 'info');
        
        const response = await axios.post('/api/service/start');
        const result = response.data;
        
        renderServiceStatus(result.status);
        showServiceMessage(result.message, result.status.status === 'running' ? 'success' : 'danger');
        
    } catch (error) {
        console.error('启动服务失败:', error);
        showServiceMessage('启动服务失败: ' + (error.response?.data?.detail || error.message), 'danger');
    } finally {
        // 启用按钮
        document.getElementById('startServiceBtn').disabled = false;
        document.getElementById('stopServiceBtn').disabled = false;
    }
}

// 停止服务
async function stopService() {
    try {
        // 禁用按钮，防止重复点击
        const startBtn = document.getElementById('startServiceBtn');
        const stopBtn = document.getElementById('stopServiceBtn');
        startBtn.disabled = true;
        stopBtn.disabled = true;
        
        showServiceMessage('正在停止服务...', 'info');
        
        const response = await axios.post('/api/service/stop');
        const result = response.data;
        
        renderServiceStatus(result.status);
        showServiceMessage(result.message, result.status.status === 'stopped' ? 'success' : 'danger');
        
    } catch (error) {
        console.error('停止服务失败:', error);
        showServiceMessage('停止服务失败: ' + (error.response?.data?.detail || error.message), 'danger');
    } finally {
        // 启用按钮
        document.getElementById('startServiceBtn').disabled = false;
        document.getElementById('stopServiceBtn').disabled = false;
    }
}

// 显示服务消息
function showServiceMessage(message, type = 'info') {
    const messageDiv = document.getElementById('serviceMessage');
    messageDiv.innerHTML = `
        <div class="alert alert-${type}" role="alert">
            ${message}
        </div>
    `;
    
    // 3秒后自动隐藏消息
    setTimeout(() => {
        messageDiv.innerHTML = '';
    }, 3000);
}

// 加载日志
async function loadLogs() {
    try {
        // 获取当前选择的日志级别
        const logLevel = document.getElementById('logLevelSelect').value;
        
        // 显示加载状态
        const logsContent = document.getElementById('logsContent');
        logsContent.textContent = '正在加载日志...';
        
        // 请求日志数据
        const response = await axios.get('/api/logs', {
            params: {
                level: logLevel,
                limit: 1000
            }
        });
        
        const result = response.data;
        
        if (result.status === 'success') {
            logsContent.textContent = result.data || '没有日志内容';
        } else {
            logsContent.textContent = `加载日志失败: ${result.detail || '未知错误'}`;
        }
    } catch (error) {
        console.error('加载日志失败:', error);
        document.getElementById('logsContent').textContent = `加载日志失败: ${error.response?.data?.detail || error.message}`;
    }
}

// 绑定事件监听器
function bindEventListeners() {
    // 搜索按钮
    document.getElementById('searchBtn').addEventListener('click', function() {
        const searchTerm = document.getElementById('toolSearch').value.toLowerCase();
        const filteredTools = originalTools.filter(tool => 
            tool.TOOL_ID.toLowerCase().includes(searchTerm) ||
            (tool.TOOL_NAME && tool.TOOL_NAME.toLowerCase().includes(searchTerm)) ||
            (tool.DESCRIPTION && tool.DESCRIPTION.toLowerCase().includes(searchTerm))
        );
        renderToolList(filteredTools);
    });
    
    // 搜索框回车键
    document.getElementById('toolSearch').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            document.getElementById('searchBtn').click();
        }
    });
    
    // 执行按钮
    document.getElementById('executeBtn').addEventListener('click', executeTool);
    
    // 重置按钮
    document.getElementById('resetBtn').addEventListener('click', function() {
        if (currentTool) {
            generateToolForm(currentTool.details.PARAM);
        }
        hideExecutionResult();
    });
    
    // 配置表单保存按钮
    document.getElementById('saveConfigBtn').addEventListener('click', saveConfig);
    
    // 配置表单重置按钮
    document.getElementById('resetConfigBtn').addEventListener('click', renderConfigForm);
    
    // 服务管理按钮
    document.getElementById('startServiceBtn').addEventListener('click', startService);
    document.getElementById('stopServiceBtn').addEventListener('click', stopService);
    document.getElementById('refreshServiceBtn').addEventListener('click', loadServiceStatus);
    
    // 日志管理按钮
    document.getElementById('refreshLogsBtn').addEventListener('click', loadLogs);
    document.getElementById('clearLogsBtn').addEventListener('click', async function() {
        try {
            // 显示确认提示
            if (confirm('确定要清空日志文件吗？此操作不可恢复。')) {
                // 调用清空日志API
                await axios.delete('/api/logs');
                // 刷新日志显示
                loadLogs();
                // 显示成功消息
                const logsContent = document.getElementById('logsContent');
                logsContent.textContent = '日志文件已清空';
            }
        } catch (error) {
            console.error('清空日志失败:', error);
            document.getElementById('logsContent').textContent = `清空日志失败: ${error.response?.data?.detail || error.message}`;
        }
    });
    document.getElementById('logLevelSelect').addEventListener('change', loadLogs);
}

// 保存配置
async function saveConfig() {
    try {
        // 获取表单数据
        const formData = new FormData(document.getElementById('configForm'));
        const config = {
            sap: {},
            mcp: {}
        };
        
        // 解析表单数据
        for (const [name, value] of formData.entries()) {
            const [section, key] = name.split('.');
            if (section && key) {
                config[section][key] = value;
            }
        }
        
        // 转换数值类型
        config.sap.client_id = parseInt(config.sap.client_id);
        config.sap.timeout = parseInt(config.sap.timeout);
        config.mcp.port = parseInt(config.mcp.port);
        
        // 发送保存请求
        const response = await axios.post('/api/config', config);
        
        // 显示保存成功消息
        showConfigMessage('配置保存成功', 'success');
        
        // 更新配置数据
        configData = config;
    } catch (error) {
        console.error('保存配置失败:', error);
        showConfigMessage('配置保存失败: ' + (error.response?.data?.detail || error.message), 'danger');
    }
}

// 显示配置消息
function showConfigMessage(message, type = 'info') {
    const messageDiv = document.getElementById('configMessage');
    messageDiv.innerHTML = `
        <div class="alert alert-${type}" role="alert">
            ${message}
        </div>
    `;
    
    // 3秒后自动隐藏消息
    setTimeout(() => {
        messageDiv.innerHTML = '';
    }, 3000);
}

// 显示错误信息
function displayError(message) {
    const toolList = document.getElementById('toolList');
    toolList.innerHTML = `
        <div class="text-center py-4">
            <div class="alert alert-danger" role="alert">
                <h5>错误</h5>
                <p>${message}</p>
                <button type="button" class="btn btn-sm btn-primary" onclick="loadToolList()">重试</button>
            </div>
        </div>
    `;
}

// 隐藏执行结果
function hideExecutionResult() {
    const executionResult = document.getElementById('executionResult');
    executionResult.style.display = 'none';
}

// 格式化JSON
function formatJSON(obj) {
    return JSON.stringify(obj, null, 2);
}