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
            <div class="d-flex justify-content-between align-items-start">
                <div>
                <h6 class="mb-1 fw-bold">${tool.TOOL_ID}</h6>
                    <p class="mb-1 text-muted small">${tool.DESCRIPTION || '无描述'}</p>
                    ${tool.TOOL_NAME ? `<p class="mb-1 text-muted small">${tool.TOOL_NAME}</p>` : ''}
                </div>
            </div>
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
    function generateFields(schema, parentPath = '', parentFullPath = '') {
        let html = '';
        
        // 遍历所有字段，生成表单
        for (const [key, value] of Object.entries(schema)) {
            const fieldName = parentPath ? `${parentPath}[${key}]` : key;
            
            // 检查当前值是否是对象
            if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
                // 检查是否是参数字段（包含name、type、value等属性）
                if (value.hasOwnProperty('name') || value.hasOwnProperty('type') || value.hasOwnProperty('value')) {
                    // 这是一个参数字段，name和type是说明，value是实际值
                    const nameValue = value.name || '';
                    const typeValue = value.type || '';
                    let actualValue = value.value !== undefined ? value.value : '';
                    
                    // 尝试自动判断输入类型
                    let inputType = 'text';
                    if (typeof actualValue === 'number') {
                        inputType = 'number';
                    } else if (typeof actualValue === 'boolean') {
                        inputType = 'checkbox';
                    }
                    
                    // 构建说明文字，将name和type显示在一起
                    let descriptionParts = [];
                    if (nameValue) {
                        descriptionParts.push(nameValue);
                    }
                    if (typeValue) {
                        descriptionParts.push(`类型: ${typeValue}`);
                    }
                    const descriptionText = descriptionParts.join(' | ');
                    
                    if (inputType === 'checkbox') {
                        // 复选框类型
                        html += `
                            <div class="mb-3 form-check">
                                <input type="${inputType}" class="form-check-input" id="${fieldName}" name="${fieldName}" ${actualValue ? 'checked' : ''}>
                                <label class="form-check-label fw-medium" for="${fieldName}">${key}</label>
                                ${descriptionText ? `<div class="form-text">${descriptionText}</div>` : ''}
                            </div>
                        `;
                    } else {
                        // 文本、数字等类型
                        html += `
                            <div class="mb-3">
                                <label for="${fieldName}" class="form-label fw-medium">${key}</label>
                                <input type="${inputType}" class="form-control" id="${fieldName}" name="${fieldName}" placeholder="${typeof actualValue === 'string' ? actualValue : JSON.stringify(actualValue)}" value="${typeof actualValue === 'string' ? actualValue : actualValue}" ${inputType === 'number' ? 'step="any"' : ''}>
                                ${descriptionText ? `<div class="form-text">${descriptionText}</div>` : ''}
                            </div>
                        `;
                    }
                } else {
                    // 这是一个嵌套对象，需要生成卡片
                    // 提取type属性（如果存在），用于说明
                    let typeValue = value.type || '';
                    
                    // 生成卡片
                    const cardId = `card-${Math.random().toString(36).substr(2, 9)}`;
                    
                    // 构建卡片标题，只显示字段名和type（如果有）
                    let cardTitle = key;
                    if (typeValue) {
                        cardTitle += ` <span class="badge bg-secondary ms-2">${typeValue}</span>`;
                    }
                    
                    html += `
                        <div class="card mb-3">
                            <div class="card-header bg-light d-flex justify-content-between align-items-center cursor-pointer" onclick="toggleCard('${cardId}')">
                                <h6 class="mb-0 text-primary">
                                    <i id="icon-${cardId}" class="bi bi-caret-down-fill"></i> ${cardTitle}
                                </h6>
                                <span class="text-muted" style="font-size: 0.85rem;">
                                    <i class="bi bi-chevron-up"></i>
                                </span>
                            </div>
                            <div id="${cardId}" class="card-body p-3">
                                ${generateFields(value, fieldName, key)}
                            </div>
                        </div>
                    `;
                }
            } else if (Array.isArray(value)) {
                // 数组字段
                html += `
                    <div class="mb-3">
                        <label for="${fieldName}" class="form-label fw-medium">${key} (数组)</label>
                        <textarea class="form-control" id="${fieldName}" name="${fieldName}" rows="3" placeholder="请输入JSON格式的数组"></textarea>
                        <div class="form-text">例如: ["value1", "value2"]</div>
                    </div>
                `;
            } else {
                // 基本类型字段
                let actualValue = value;
                
                // 尝试自动判断输入类型
                let inputType = 'text';
                if (typeof actualValue === 'number') {
                    inputType = 'number';
                } else if (typeof actualValue === 'boolean') {
                    inputType = 'checkbox';
                }
                
                // 构建类型描述
                let typeDescription = `类型: ${typeof actualValue}`;
                
                if (inputType === 'checkbox') {
                    // 复选框类型
                    html += `
                        <div class="mb-3 form-check">
                            <input type="${inputType}" class="form-check-input" id="${fieldName}" name="${fieldName}" ${actualValue ? 'checked' : ''}>
                            <label class="form-check-label fw-medium" for="${fieldName}">${key}</label>
                            <div class="form-text">${typeDescription}</div>
                        </div>
                    `;
                } else {
                    // 文本、数字等类型
                    html += `
                        <div class="mb-3">
                            <label for="${fieldName}" class="form-label fw-medium">${key}</label>
                            <input type="${inputType}" class="form-control" id="${fieldName}" name="${fieldName}" placeholder="${typeof actualValue === 'string' ? actualValue : JSON.stringify(actualValue)}" value="${typeof actualValue === 'string' ? actualValue : actualValue}" ${inputType === 'number' ? 'step="any"' : ''}>
                            <div class="form-text">${typeDescription}</div>
                        </div>
                    `;
                }
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
        showExecutionResult('正在执行工具，请稍候...', true);
        
        // 构建请求报文，将参数放在PARAM对象下
        const requestPayload = {
            TOOL_ID: currentTool.id,
            PARAM: params
        };
        
        // 显示请求报文（用于调试）
        console.log('请求报文:', JSON.stringify(requestPayload, null, 2));
        
        // 执行工具
        const response = await axios.post(`/api/tools/${currentTool.id}/use`, requestPayload);
        
        // 显示结果
        showExecutionResult(JSON.stringify(response.data, null, 2));
    } catch (error) {
        console.error('执行工具失败:', error);
        const errorMessage = error.response?.data?.detail || error.message;
        showExecutionResult('执行失败: ' + errorMessage, true);
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

// 删除对象中的默认值
function removeDefaultValues(obj) {
    if (typeof obj !== 'object' || obj === null) {
        return obj;
    }
    
    // 处理数组
    if (Array.isArray(obj)) {
        return obj.map(item => removeDefaultValues(item));
    }
    
    // 处理对象
    const result = {};
    for (const [key, value] of Object.entries(obj)) {
        // 递归处理嵌套对象
        const processedValue = removeDefaultValues(value);
        
        // 删除默认值
        if (processedValue !== undefined && processedValue !== null && processedValue !== '' && 
            !(Array.isArray(processedValue) && processedValue.length === 0) &&
            !(typeof processedValue === 'object' && Object.keys(processedValue).length === 0)) {
            result[key] = processedValue;
        }
    }
    
    return result;
}

// 格式化并高亮JSON结果
function formatAndHighlightJSON(jsonString) {
    try {
        const obj = typeof jsonString === 'string' ? JSON.parse(jsonString) : jsonString;
        
        // 删除默认值
        const simplifiedObj = removeDefaultValues(obj);
        
        // 格式化JSON
        const formatted = JSON.stringify(simplifiedObj, null, 2);
        
        // 高亮处理：为TYPE字段添加特殊样式
        return formatted.replace(/"TYPE"\s*:\s*"([^"]+)"/g, '<span class="json-type-highlight">"TYPE": "$1"</span>');
    } catch {
        return jsonString;
    }
}

// 显示执行结果
function showExecutionResult(result, isError = false) {
    const executionResult = document.getElementById('executionResult');
    const resultOutput = document.getElementById('resultOutput');
    const resultTime = document.getElementById('resultTime');
    const resultStatus = document.getElementById('resultStatus');
    
    // 设置时间戳
    const now = new Date();
    resultTime.textContent = `执行时间: ${now.toLocaleString('zh-CN')}`;
    
    // 设置状态徽章
    resultStatus.textContent = isError ? '失败' : '成功';
    resultStatus.className = `badge ${isError ? 'bg-danger' : 'bg-success'}`;
    
    // 尝试解析并格式化JSON结果
    let displayContent = result;
    try {
        // 如果是字符串，尝试解析为JSON
        if (typeof result === 'string') {
            const parsed = JSON.parse(result);
            displayContent = JSON.stringify(parsed, null, 2);
        } else if (typeof result === 'object') {
            // 如果是对象，直接格式化
            displayContent = JSON.stringify(result, null, 2);
        }
    } catch (e) {
        // 如果解析失败，使用原始内容
        displayContent = result;
    }
    
    // 设置输出内容
    resultOutput.textContent = displayContent;
    resultOutput.className = isError ? 'bg-danger text-white p-3 rounded' : 'bg-light p-3 rounded';
    resultOutput.style.whiteSpace = 'pre-wrap';
    resultOutput.style.wordBreak = 'break-word';
    resultOutput.style.maxHeight = '400px';
    resultOutput.style.overflow = 'auto';
    
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
    console.log('switchPage 被调用，pageName:', pageName);
    // 隐藏所有页面
    document.getElementById('toolsPage').style.display = 'none';
    document.getElementById('configPage').style.display = 'none';
    document.getElementById('servicePage').style.display = 'none';
    document.getElementById('logsPage').style.display = 'none';
    
    console.log('开始显示页面:', pageName);
    // 显示对应的页面
    if (pageName == '工具管理') {
        document.getElementById('toolsPage').style.display = 'block';
        // 加载工具列表
        loadToolList();
    } else if (pageName == '服务器配置') {
        document.getElementById('configPage').style.display = 'block';
        // 确保配置数据已加载
        if (!configData) {
            loadConfigData();
        }
    } else if (pageName == '服务管理') {
        document.getElementById('servicePage').style.display = 'block';
        // 加载服务状态
        loadServiceStatus();
    } else if (pageName == '日志查看') {
        document.getElementById('logsPage').style.display = 'block';
        // 加载日志
        loadLogs();
    }
    console.log('页面切换完成');
}

// 加载配置数据
async function loadConfigData() {
    try {
        const response = await axios.get('/api/config');
        const result = response.data;
        
        if (result.config && result.sap_config) {
            configData = {
                sap: result.sap_config,
                mcp: result.config,
                web: result.web_config
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
    console.log('renderConfigForm 被调用');
    console.log('configData:', configData);
    if (!configData) {
        console.log('configData 为空，跳过渲染');
        return;
    }
    
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
    
    // 设置WEB服务器配置
    if (configData.web) {
        document.getElementById('webHost').value = configData.web.host;
        document.getElementById('webPort').value = configData.web.port;
        document.getElementById('webReload').checked = configData.web.reload;
    }
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
    
    // 参数折叠/展开按钮
    document.getElementById('toggleParamsBtn').addEventListener('click', function() {
        const paramsContainer = document.getElementById('paramsContainer');
        const button = this;
        const icon = button.querySelector('i');
        const text = button.textContent.trim().replace('隐藏参数', '').replace('显示参数', '');
        
        if (paramsContainer.style.display === 'none') {
            paramsContainer.style.display = 'block';
            button.innerHTML = `<i class="bi bi-chevron-down"></i> 隐藏参数`;
        } else {
            paramsContainer.style.display = 'none';
            button.innerHTML = `<i class="bi bi-chevron-right"></i> 显示参数`;
        }
    });
    
    // 复制结果按钮
    document.getElementById('copyResultBtn').addEventListener('click', function() {
        const resultOutput = document.getElementById('resultOutput');
        navigator.clipboard.writeText(resultOutput.textContent)
            .then(() => {
                const originalText = this.textContent;
                this.textContent = '已复制';
                setTimeout(() => {
                    this.innerHTML = `<i class="bi bi-clipboard"></i> 复制`;
                }, 1500);
            })
            .catch(err => {
                console.error('复制失败:', err);
            });
    });
    
    // 下载结果按钮
    document.getElementById('downloadResultBtn').addEventListener('click', function() {
        const resultOutput = document.getElementById('resultOutput');
        const now = new Date();
        const timestamp = now.toISOString().slice(0, 19).replace(/:/g, '-');
        const filename = `tool-result-${timestamp}.txt`;
        
        const blob = new Blob([resultOutput.textContent], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });
    
    // 关闭结果按钮
    document.getElementById('closeResultBtn').addEventListener('click', hideExecutionResult);
    
    // 配置表单保存按钮 - 使用可选链操作符，因为按钮已被替换为每个配置块的独立按钮
    document.getElementById('saveConfigBtn')?.addEventListener('click', saveConfig);
    
    // 配置表单重置按钮 - 使用可选链操作符，因为按钮已被替换为每个配置块的独立按钮
    document.getElementById('resetConfigBtn')?.addEventListener('click', renderConfigForm);
    
    // 接口测试按钮 - 使用可选链操作符，因为按钮已被替换为每个配置块的独立按钮
    document.getElementById('testApiBtn')?.addEventListener('click', testApi);
    
    // 密码显示/隐藏切换按钮
    document.getElementById('togglePassword')?.addEventListener('click', function() {
        const passwordInput = document.getElementById('sapPassword');
        const icon = this;
        
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            icon.textContent = '🙈';
        } else {
            passwordInput.type = 'password';
            icon.textContent = '👁️';
        }
    });
    
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
            mcp: {},
            web: {}
        };
        
        // 解析表单数据
        for (const [name, value] of formData.entries()) {
            const [section, key] = name.split('.');
            if (section && key) {
                config[section][key] = value;
            }
        }
        
        // 处理复选框
        const webReloadCheckbox = document.getElementById('webReload');
        config.web.reload = webReloadCheckbox.checked;
        
        // 转换数值类型
        config.sap.client_id = parseInt(config.sap.client_id);
        config.sap.timeout = parseInt(config.sap.timeout);
        config.mcp.port = parseInt(config.mcp.port);
        config.web.port = parseInt(config.web.port);
        
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

// 保存单个配置块
async function saveConfigSection(section) {
    try {
        // 获取该配置块的所有字段
        const formData = new FormData(document.getElementById('configForm'));
        const config = {};
        config[section] = {};
        
        // 解析该配置块的表单数据
        for (const [name, value] of formData.entries()) {
            const [fieldSection, key] = name.split('.');
            if (fieldSection === section && key) {
                config[section][key] = value;
            }
        }
        
        // 处理复选框（仅WEB配置）
        if (section === 'web') {
            const webReloadCheckbox = document.getElementById('webReload');
            config.web.reload = webReloadCheckbox.checked;
        }
        
        // 转换数值类型
        if (section === 'sap') {
            config.sap.client_id = parseInt(config.sap.client_id);
            config.sap.timeout = parseInt(config.sap.timeout);
        } else if (section === 'mcp') {
            config.mcp.port = parseInt(config.mcp.port);
        } else if (section === 'web') {
            config.web.port = parseInt(config.web.port);
        }
        
        // 发送保存请求
        const response = await axios.post('/api/config', config);
        
        // 显示保存成功消息
        showConfigMessage(`${section.toUpperCase()}配置保存成功`, 'success');
        
        // 更新配置数据
        if (!configData) {
            configData = {
                sap: {},
                mcp: {},
                web: {}
            };
        }
        configData[section] = config[section];
    } catch (error) {
        console.error(`保存${section}配置失败:`, error);
        showConfigMessage(`${section.toUpperCase()}配置保存失败: ` + (error.response?.data?.detail || error.message), 'danger');
    }
}

// 重置单个配置块
function resetConfigSection(section) {
    try {
        // 从配置数据中获取该配置块的原始值
        if (configData && configData[section]) {
            const sectionConfig = configData[section];
            
            // 重置该配置块的所有字段
            for (const [key, value] of Object.entries(sectionConfig)) {
                const fieldId = `${section}${key.charAt(0).toUpperCase() + key.slice(1)}`;
                const element = document.getElementById(fieldId);
                
                if (element) {
                    if (element.type === 'checkbox') {
                        element.checked = value;
                    } else {
                        element.value = value;
                    }
                }
            }
            
            showConfigMessage(`${section.toUpperCase()}配置已重置`, 'info');
        }
    } catch (error) {
        console.error(`重置${section}配置失败:`, error);
        showConfigMessage(`${section.toUpperCase()}配置重置失败: ${error.message}`, 'danger');
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
    
    // 滚动到消息区域，确保用户能看到
    messageDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    // 5秒后自动隐藏消息（增加显示时间）
    setTimeout(() => {
        messageDiv.innerHTML = '';
    }, 5000);
}

// 折叠/展开卡片
function toggleCard(cardId) {
    const cardBody = document.getElementById(cardId);
    const icon = document.getElementById(`icon-${cardId}`);
    
    if (cardBody.style.display === 'none') {
        // 展开卡片
        cardBody.style.display = 'block';
        icon.className = 'bi bi-caret-down-fill';
    } else {
        // 折叠卡片
        cardBody.style.display = 'none';
        icon.className = 'bi bi-caret-right-fill';
    }
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

// 测试API连接
async function testApi() {
    const apiStatus = document.getElementById('apiStatus');
    
    try {
        // 更新状态显示
        apiStatus.innerHTML = '<span class="text-warning">测试中...</span>';
        
        // 调用API测试接口
        const response = await axios.post('/api/test-api');
        const result = response.data;
        
        if (result.success) {
            // 测试成功
            apiStatus.innerHTML = '<span class="text-success">测试成功</span>';
            showConfigMessage('接口测试成功', 'success');
        } else {
            // 测试失败
            apiStatus.innerHTML = '<span class="text-danger">测试失败</span>';
            showConfigMessage('接口测试失败: ' + result.message, 'danger');
        }
    } catch (error) {
        // 请求失败
        apiStatus.innerHTML = '<span class="text-danger">请求失败</span>';
        showConfigMessage('接口测试失败: ' + (error.response?.data?.message || error.message), 'danger');
    }
}

// 格式化JSON
function formatJSON(obj) {
    return JSON.stringify(obj, null, 2);
}