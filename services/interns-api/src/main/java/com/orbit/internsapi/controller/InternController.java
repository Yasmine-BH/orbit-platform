package com.orbit.internsapi.controller;

import com.orbit.internsapi.dto.CreateInternRequest;
import com.orbit.internsapi.dto.InternResponse;
import com.orbit.internsapi.dto.UpdateInternRequest;
import com.orbit.internsapi.service.InternService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/interns")
@Tag(name = "Interns", description = "Manage the list of interns")
public class InternController {

    private final InternService internService;

    public InternController(InternService internService) {
        this.internService = internService;
    }

    @PostMapping
    @Operation(summary = "Create a new intern")
    public ResponseEntity<InternResponse> create(@Valid @RequestBody CreateInternRequest request) {
        InternResponse created = internService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    @GetMapping
    @Operation(summary = "List all interns")
    public ResponseEntity<List<InternResponse>> findAll() {
        return ResponseEntity.ok(internService.findAll());
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get an intern by id")
    public ResponseEntity<InternResponse> findById(@PathVariable Long id) {
        return ResponseEntity.ok(internService.findById(id));
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update an existing intern")
    public ResponseEntity<InternResponse> update(@PathVariable Long id,
                                                  @Valid @RequestBody UpdateInternRequest request) {
        return ResponseEntity.ok(internService.update(id, request));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete an intern")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        internService.delete(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/{id}/exists")
    @Operation(summary = "Check whether an intern exists (used by tasks-api before creating a task)")
    public ResponseEntity<Void> exists(@PathVariable Long id) {
        return internService.existsById(id)
                ? ResponseEntity.ok().build()
                : ResponseEntity.notFound().build();
    }
}
