settings = {
    "settings": {
        "index": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "mapping.depth.limit": 500,
		    "mapping.total_fields.limit" : 50000,
		    "mapping.nested_fields.limit" : 50000
        }
    },
    "mappings": {
        "properties": {
            "date_time": {
                "type": "date",
                "format": "EEE MMM d[d] HH:mm:ss yyyy"
            },
			"references": {
				"type" : "object",
				"enabled" : "false"
			},
			"advisories": {
				"type" : "object",
				"enabled" : "false"
			},
			"findings": {
				"type" : "object",
				"enabled" : "false"
			},
            "summary": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 8192
                    }
                }
            },
            "check": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 8192
                    }
                }
            },
            "fix": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 8192
                    }
                }
            },
            "description": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 8192
                    }
                }
            },
            "impact": {
                "properties": {
                    "description": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 8192
                            }
                        }
                    }
                }
            },
            "reccomendation": {
                "properties": {
                    "description": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 8192
                            }
                        }
                    }
                }
            },
            "ease": {
                "properties": {
                    "description": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 8192
                            }
                        }
                    }
                }
            }
        }
    }
}
